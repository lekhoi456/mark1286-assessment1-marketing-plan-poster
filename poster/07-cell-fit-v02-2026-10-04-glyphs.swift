import Foundation
import CoreText
import CoreGraphics

func number(_ value: CGFloat) -> String { String(format: "%.3f", Double(value)) }

func pathData(_ path: CGPath) -> String {
    var commands: [String] = []
    path.applyWithBlock { pointer in
        let element = pointer.pointee
        let points = element.points
        switch element.type {
        case .moveToPoint: commands.append("M\(number(points[0].x)) \(number(points[0].y))")
        case .addLineToPoint: commands.append("L\(number(points[0].x)) \(number(points[0].y))")
        case .addQuadCurveToPoint:
            commands.append("Q\(number(points[0].x)) \(number(points[0].y)) \(number(points[1].x)) \(number(points[1].y))")
        case .addCurveToPoint:
            commands.append("C\(number(points[0].x)) \(number(points[0].y)) \(number(points[1].x)) \(number(points[1].y)) \(number(points[2].x)) \(number(points[2].y))")
        case .closeSubpath: commands.append("Z")
        @unknown default: break
        }
    }
    return commands.joined(separator: " ")
}

func outline(_ request: [String: Any]) throws -> [String: Any] {
    guard let text = request["text"] as? String,
          let fontName = request["font"] as? String,
          let size = request["size"] as? Double else {
        throw NSError(domain: "glyphs", code: 1, userInfo: [NSLocalizedDescriptionKey: "Invalid request"])
    }
    let font = CTFontCreateWithName(fontName as CFString, CGFloat(size), nil)
    let attributes: [NSAttributedString.Key: Any] = [NSAttributedString.Key(kCTFontAttributeName as String): font]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: text, attributes: attributes))
    let width = CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil))
    let runs = CTLineGetGlyphRuns(line) as! [CTRun]
    let combined = CGMutablePath()
    var resolvedFonts = Set<String>()
    for run in runs {
        let count = CTRunGetGlyphCount(run)
        var glyphs = [CGGlyph](repeating: 0, count: count)
        var positions = [CGPoint](repeating: .zero, count: count)
        CTRunGetGlyphs(run, CFRange(location: 0, length: 0), &glyphs)
        CTRunGetPositions(run, CFRange(location: 0, length: 0), &positions)
        let attributes = CTRunGetAttributes(run) as NSDictionary
        guard let runFont = attributes[kCTFontAttributeName as String] else { continue }
        let ctFont = runFont as! CTFont
        let resolvedName = CTFontCopyPostScriptName(ctFont) as String
        let span = CTRunGetStringRange(run)
        let runText = (text as NSString).substring(with: NSRange(location: span.location, length: span.length))
        if runText.allSatisfy({ $0 == "×" || $0 == "≥" }) {
            resolvedFonts.insert("Native vector maths")
            for (index, character) in runText.enumerated() {
                let x = positions[index].x
                let y = positions[index].y + CGFloat(size) * 0.1
                let w = CGFloat(size) * 0.5
                let h = CGFloat(size) * 0.5
                let symbol = CGMutablePath()
                if character == "×" {
                    symbol.move(to: CGPoint(x:x,y:y))
                    symbol.addLine(to: CGPoint(x:x+w,y:y+h))
                    symbol.move(to: CGPoint(x:x+w,y:y))
                    symbol.addLine(to: CGPoint(x:x,y:y+h))
                } else {
                    symbol.move(to: CGPoint(x:x,y:y+h))
                    symbol.addLine(to: CGPoint(x:x+w,y:y+h*0.65))
                    symbol.addLine(to: CGPoint(x:x,y:y+h*0.3))
                    symbol.move(to: CGPoint(x:x,y:y))
                    symbol.addLine(to: CGPoint(x:x+w,y:y))
                }
                combined.addPath(symbol.copy(strokingWithWidth: CGFloat(size)*0.07, lineCap: .round, lineJoin: .round, miterLimit: 1))
            }
            continue
        }
        if runText.allSatisfy({ $0 == "→" }) {
            resolvedFonts.insert("Native vector arrow")
            for index in 0..<count {
                let x = positions[index].x
                let y = positions[index].y + CGFloat(size) * 0.28
                let w = CGFloat(size) * 0.82
                let h = CGFloat(size) * 0.23
                combined.move(to: CGPoint(x:x,y:y-h*0.15))
                combined.addLine(to: CGPoint(x:x+w*0.66,y:y-h*0.15))
                combined.addLine(to: CGPoint(x:x+w*0.54,y:y-h))
                combined.addLine(to: CGPoint(x:x+w,y:y))
                combined.addLine(to: CGPoint(x:x+w*0.54,y:y+h))
                combined.addLine(to: CGPoint(x:x+w*0.66,y:y+h*0.15))
                combined.addLine(to: CGPoint(x:x,y:y+h*0.15))
                combined.closeSubpath()
            }
            continue
        }
        resolvedFonts.insert(resolvedName)
        for index in 0..<count {
            if let glyph = CTFontCreatePathForGlyph(ctFont, glyphs[index], nil) {
                var transform = CGAffineTransform(translationX: positions[index].x, y: positions[index].y)
                if let positioned = glyph.copy(using: &transform) { combined.addPath(positioned) }
            }
        }
    }
    let bounds = combined.boundingBoxOfPath
    return ["text": text, "resolved_font_names": Array(resolvedFonts).sorted(), "width": Double(width), "path": pathData(combined),
            "bounds": [Double(bounds.minX), Double(bounds.minY), Double(bounds.maxX), Double(bounds.maxY)]]
}

while let line = readLine() {
    do {
        guard let data = line.data(using: .utf8),
              let request = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            throw NSError(domain: "glyphs", code: 2, userInfo: [NSLocalizedDescriptionKey: "Invalid JSON"])
        }
        let response = try outline(request)
        let encoded = try JSONSerialization.data(withJSONObject: response, options: [.fragmentsAllowed, .sortedKeys])
        FileHandle.standardOutput.write(encoded)
        FileHandle.standardOutput.write(Data([0x0A]))
    } catch {
        let encoded = try! JSONSerialization.data(withJSONObject: ["error": error.localizedDescription])
        FileHandle.standardOutput.write(encoded)
        FileHandle.standardOutput.write(Data([0x0A]))
    }
}

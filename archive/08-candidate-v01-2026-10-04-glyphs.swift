import Foundation
import CoreText
import CoreGraphics

func number(_ value: CGFloat) -> String {
    String(format: "%.3f", Double(value))
}

func pathData(_ path: CGPath) -> String {
    var commands: [String] = []
    path.applyWithBlock { elementPointer in
        let element = elementPointer.pointee
        let points = element.points
        switch element.type {
        case .moveToPoint:
            commands.append("M\(number(points[0].x)) \(number(points[0].y))")
        case .addLineToPoint:
            commands.append("L\(number(points[0].x)) \(number(points[0].y))")
        case .addQuadCurveToPoint:
            commands.append("Q\(number(points[0].x)) \(number(points[0].y)) \(number(points[1].x)) \(number(points[1].y))")
        case .addCurveToPoint:
            commands.append("C\(number(points[0].x)) \(number(points[0].y)) \(number(points[1].x)) \(number(points[1].y)) \(number(points[2].x)) \(number(points[2].y))")
        case .closeSubpath:
            commands.append("Z")
        @unknown default:
            break
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

    for run in runs {
        let runCount = CTRunGetGlyphCount(run)
        var glyphs = [CGGlyph](repeating: 0, count: runCount)
        var positions = [CGPoint](repeating: .zero, count: runCount)
        CTRunGetGlyphs(run, CFRange(location: 0, length: 0), &glyphs)
        CTRunGetPositions(run, CFRange(location: 0, length: 0), &positions)
        let attributes = CTRunGetAttributes(run) as NSDictionary
        guard let runFont = attributes[kCTFontAttributeName as String] else { continue }
        let ctRunFont = runFont as! CTFont
        if CTFontCopyPostScriptName(ctRunFont) != CTFontCopyPostScriptName(font) {
            let range = CTRunGetStringRange(run)
            let runText = (text as NSString).substring(with: NSRange(location: range.location, length: range.length))
            guard runText.allSatisfy({ $0 == "→" || $0.isWhitespace }) else {
                throw NSError(domain: "glyphs", code: 3, userInfo: [NSLocalizedDescriptionKey: "Unexpected ordinary-font fallback"])
            }
            // The arrow is a controlled pen-shaped vector; no substitute lettering face.
            for position in positions {
                let x = position.x, y = position.y + CGFloat(size) * 0.30
                let s = CGFloat(size)
                let points = [CGPoint(x:x+2,y:y-1.2), CGPoint(x:x+s*0.55,y:y-0.8),
                    CGPoint(x:x+s*0.43,y:y+s*0.13), CGPoint(x:x+s*0.49,y:y+s*0.17),
                    CGPoint(x:x+s*0.68,y:y), CGPoint(x:x+s*0.49,y:y-s*0.16),
                    CGPoint(x:x+s*0.43,y:y-s*0.12), CGPoint(x:x+s*0.55,y:y+0.9),
                    CGPoint(x:x+2,y:y+1.3)]
                combined.move(to: points[0])
                for point in points.dropFirst() { combined.addLine(to: point) }
                combined.closeSubpath()
            }
            continue
        }
        for index in 0..<runCount {
            if let glyphPath = CTFontCreatePathForGlyph(ctRunFont, glyphs[index], nil) {
                var transform = CGAffineTransform(translationX: positions[index].x, y: positions[index].y)
                if let positioned = glyphPath.copy(using: &transform) {
                    combined.addPath(positioned)
                }
            }
        }
    }

    let bounds = combined.boundingBoxOfPath
    return [
        "text": text,
        "width": Double(width),
        "path": pathData(combined),
        "bounds": [Double(bounds.minX), Double(bounds.minY), Double(bounds.maxX), Double(bounds.maxY)],
        "resolved_font": CTFontCopyPostScriptName(font) as String,
        "font_file": (CTFontCopyAttribute(font, kCTFontURLAttribute) as? URL)?.path ?? "unknown",
        "run_fonts": runs.map { run in
            let attrs = CTRunGetAttributes(run) as NSDictionary
            let runFont = attrs[kCTFontAttributeName as String] as! CTFont
            let name = CTFontCopyPostScriptName(runFont) as String
            return name == fontName ? name : "controlled-arrow-vector"
        },
    ]
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
        let error = ["error": error.localizedDescription]
        let encoded = try! JSONSerialization.data(withJSONObject: error, options: [.fragmentsAllowed])
        FileHandle.standardOutput.write(encoded)
        FileHandle.standardOutput.write(Data([0x0A]))
    }
}

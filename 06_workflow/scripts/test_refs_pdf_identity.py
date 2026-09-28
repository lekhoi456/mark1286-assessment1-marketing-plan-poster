#!/usr/bin/env python3
"""Isolated PDF-identity regressions; synthetic PDFs, never live acceptance records.

Run: python3 -B -m unittest discover -s 06_workflow/scripts -p 'test_refs_pdf_identity.py' -v
Requires the same pdftotext executable as refs.py verify.
"""
import argparse
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import refs


def fixture_pdf(path, lines):
    """Write a real, one-page PDF with a controlled text layer for Poppler."""
    escaped = [line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)') for line in lines]
    stream = ('BT /F1 12 Tf 40 740 Td 18 TL ' + ' T* '.join(f'({line}) Tj' for line in escaped) + ' ET').encode('ascii')
    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        f'<< /Length {len(stream)} >>\nstream\n'.encode() + stream + b'\nendstream',
    ]
    data = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f'{index} 0 obj\n'.encode() + obj + b'\nendobj\n')
    start = len(data)
    data.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:
        data.extend(f'{offset:010d} 00000 n \n'.encode())
    data.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode())
    path.write_bytes(data)


class ManualPdfIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='refs-identity-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = patch.multiple(refs, REF_DIR=self.root, ARCHIVE_DIR=self.root / '_archived',
                                    INBOX_DIR=self.root / '_inbox', REGISTRY=self.root / 'references.json',
                                    HTML_OUT=self.root / 'references.html', MD_OUT=self.root / 'reference-list.md',
                                    DRAFT_DIRS=[])
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.entry = {
            'key': 'fixture-agency-2026', 'type': 'dataset', 'status': 'cited',
            'organisation': 'Fixture Agency', 'title': 'Stock vehicles registered taxis',
            'year': '2026', 'url': 'https://example.invalid/table', 'accessed': '2026-09-28',
            'file': 'fixture-agency-2026-stock.pdf', 'retrieval': {'method': 'web-snapshot'},
        }
        self.path = self.root / self.entry['file']
        self.lines = [self.entry['title'], 'Accessed: 28 September 2026', self.entry['url']]
        fixture_pdf(self.path, self.lines)
        self.verify_and_accept()

    def verify_and_accept(self):
        automatic = refs.check_pdf(self.entry, self.path)
        self.entry.setdefault('verification', {})['pdf_text'] = automatic
        self.entry['pdf_identity_accept'] = {
            'sha256': refs.pdf_sha256(self.path),
            'identity_sha256': refs.pdf_identity_sha256(self.entry),
            'fields': ['author'], 'checked_on': refs.today(),
            'verified_by': 'Synthetic regression fixture',
            'locator': 'Synthetic PDF p. 1, table title and source URL',
            'evidence': 'Synthetic fixture generator supplies the title and source URL; no real inspection claimed.',
            'reason': 'Synthetic author intentionally omitted from the text layer.',
        }

    def save(self):
        refs.save_registry({'meta': {}, 'entries': [self.entry]})

    def check_draft(self):
        draft = self.root / 'draft.md'
        draft.write_text(f"(Fixture Agency, {self.entry['year']}).\n\n## References\n\n" +
                         refs.segs_md(refs.render(self.entry).segs) + '\n', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            return refs.cmd_check_draft(argparse.Namespace(draft=str(draft)))

    def test_manual_acceptance_preserves_automatic_and_passes_consumers(self):
        original = copy.deepcopy(self.entry['verification']['pdf_text'])
        state = refs.pdf_state(self.entry)
        self.assertEqual(state['status'], 'accepted-manual')
        self.assertEqual(state['automatic'], original)
        self.assertEqual(original['status'], 'mismatch')
        self.assertEqual(original['mismatch_fields'], ['author'])
        self.save()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 0)
            self.assertEqual(refs.cmd_build(None), 0)
        stored = json.loads(refs.REGISTRY.read_text())['entries'][0]
        self.assertEqual(stored['verification']['pdf_text']['status'], 'mismatch')
        self.assertEqual(self.check_draft(), 0)

    def test_title_omission_requires_explicit_title_acceptance(self):
        fixture_pdf(self.path, ['Fixture Agency', 'Accessed: 28 September 2026'])
        self.verify_and_accept()
        self.assertNotIn(refs.pdf_state(self.entry)['status'], refs.PDF_VERIFIED)
        self.entry['pdf_identity_accept']['fields'] = ['title']
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'accepted-manual')

    def test_changed_bytes_and_missing_pdf_block_build_and_draft(self):
        self.path.write_bytes(self.path.read_bytes() + b'\n% changed bytes\n')
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')
        self.save()
        self.assertEqual(self.check_draft(), 1)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(refs.cmd_build(None), 1)
            self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 1)
        self.path.unlink()
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def test_each_identity_field_change_invalidates_acceptance(self):
        changes = {'title': 'Other title', 'authors': [{'family': 'Other'}],
                   'editors': [{'family': 'Editor'}], 'organisation': 'Other organisation',
                   'year': '2025', 'type': 'report', 'accessed': '2026-09-27',
                   'url': 'https://example.invalid/other', 'doi': '10.1234/other'}
        for field, value in changes.items():
            with self.subTest(field=field):
                entry = copy.deepcopy(self.entry)
                entry[field] = value
                self.assertEqual(refs.pdf_state(entry)['status'], 'error')
        entry = copy.deepcopy(self.entry)
        entry['retrieval']['method'] = 'open-access'
        self.assertEqual(refs.pdf_state(entry)['status'], 'error')

    def test_invalid_and_missing_snapshot_stamps_cannot_be_accepted(self):
        for stamp in ('', 'Accessed: 27 September 2026', 'Accessed: 31 September 2026'):
            with self.subTest(stamp=stamp):
                fixture_pdf(self.path, [self.entry['title'], stamp])
                self.verify_and_accept()
                self.assertIn('accessed', self.entry['verification']['pdf_text']['mismatch_fields'])
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')
        for accessed in (None, '', '2026-02-30'):
            with self.subTest(accessed=accessed):
                self.entry['accessed'] = accessed
                self.verify_and_accept()
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def test_wrong_header_and_unknown_type_cannot_be_accepted_even_if_rebound(self):
        self.path.write_bytes(b'not a PDF')
        self.verify_and_accept()
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')
        fixture_pdf(self.path, self.lines)
        self.entry['type'] = 'unknown-type'
        self.verify_and_accept()
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def test_malformed_audit_records_fail_closed(self):
        valid = copy.deepcopy(self.entry['pdf_identity_accept'])
        records = [None, False, [], 'approved', {}, {**valid, 'extra': 'blanket override'}]
        records += [{**valid, field: value} for field, value in (
            ('fields', ['year']), ('fields', []), ('fields', ['author', 'author']),
            ('fields', [{}]), ('fields', 'author'), ('checked_on', '2026-02-30'),
            ('checked_on', '9999-01-01'), ('checked_on', False), ('verified_by', ''),
            ('locator', []), ('evidence', ' '), ('reason', None), ('sha256', '123'),
            ('identity_sha256', 123))]
        for record in records:
            with self.subTest(record=record):
                self.entry['pdf_identity_accept'] = record
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def test_manual_record_cannot_upgrade_unchecked_or_error_result(self):
        for automatic in ({}, {'status': 'error', 'error': 'pdftotext failed'},
                          {'status': 'accepted-manual'}, {'status': 'match'}):
            with self.subTest(automatic=automatic):
                self.entry['verification']['pdf_text'] = automatic
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def test_no_blanket_acceptance_without_audit(self):
        del self.entry['pdf_identity_accept']
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'mismatch')
        self.entry['verification']['pdf_text']['status'] = 'accepted-manual'
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')

    def make_automatic_match(self):
        self.entry.pop('pdf_identity_accept', None)
        fixture_pdf(self.path, self.lines + ['Fixture Agency'])
        self.entry['verification']['pdf_text'] = refs.check_pdf(self.entry, self.path)
        self.assertEqual(refs.pdf_state(self.entry)['status'], 'match')

    def test_automatic_match_cannot_survive_date_edit_or_replaced_pdf(self):
        self.make_automatic_match()
        original = copy.deepcopy(self.entry)
        for change in ('accessed', 'bytes'):
            with self.subTest(change=change):
                self.entry = copy.deepcopy(original)
                if change == 'accessed':
                    self.entry['accessed'] = '2026-09-27'
                else:
                    fixture_pdf(self.path, ['Unrelated work', 'Different Agency'])
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')
                self.save()
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(refs.cmd_build(None), 1)
                self.assertEqual(self.check_draft(), 1)

    def test_automatic_match_requires_both_current_bindings(self):
        self.make_automatic_match()
        original = copy.deepcopy(self.entry)
        for field in ('sha256', 'identity_sha256'):
            with self.subTest(field=field):
                self.entry = copy.deepcopy(original)
                del self.entry['verification']['pdf_text'][field]
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'error')
                self.save()
                self.assertEqual(self.check_draft(), 1)

    def test_crossref_cache_rejects_year_and_doi_edits_after_offline_verify(self):
        self.entry['doi'] = '10.1234/fixture'
        self.make_automatic_match()
        self.save()
        message = {'DOI': self.entry['doi'], 'title': [self.entry['title']],
                   'issued': {'date-parts': [[2026]]}, 'author': []}
        with patch.object(refs, 'crossref_record', return_value=message), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=False)), 0)
        original = json.loads(refs.REGISTRY.read_text())['entries'][0]
        self.entry = copy.deepcopy(original)
        self.assertEqual(refs.crossref_state(self.entry)['status'], 'match')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 0)
        self.assertEqual(self.check_draft(), 0)
        for field, value in (('year', '2025'), ('doi', '10.1234/another-work')):
            with self.subTest(field=field):
                self.entry = copy.deepcopy(original)
                self.entry[field] = value
                self.save()
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 1)
                self.entry = json.loads(refs.REGISTRY.read_text())['entries'][0]
                self.assertEqual(refs.pdf_state(self.entry)['status'], 'match')
                self.assertEqual(refs.crossref_state(self.entry)['status'], 'error')
                self.assertEqual(self.check_draft(), 1)
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(refs.cmd_build(None), 1)

    def test_legacy_unbound_crossref_match_requires_online_verification(self):
        self.entry['doi'] = '10.1234/fixture'
        self.make_automatic_match()
        self.entry['verification']['crossref'] = {'status': 'match', 'differences': []}
        self.save()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 1)
        self.assertEqual(refs.crossref_state(self.entry)['status'], 'error')
        self.assertEqual(self.check_draft(), 1)

    def test_crossref_doi_year_authors_remain_blocking(self):
        self.entry['doi'] = '10.1234/fixture'
        self.verify_and_accept()
        for field in ('doi', 'year', 'authors'):
            with self.subTest(field=field):
                self.entry['verification']['crossref'] = {
                    'status': 'mismatch', 'differences': [f'{field}: registry differs from Crossref'],
                    'identity_sha256': refs.crossref_identity_sha256(self.entry)}
                self.entry['verification_accept'] = [
                    {'field': field, 'accepted_on': refs.today(), 'reason': 'Cannot override identity'}]
                self.assertEqual(refs.crossref_state(self.entry)['status'], 'mismatch')
                self.save()
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(refs.cmd_verify(argparse.Namespace(key=None, offline=True)), 1)
                    self.assertEqual(refs.cmd_build(None), 1)
                self.assertEqual(self.check_draft(), 1)


if __name__ == '__main__':
    unittest.main()

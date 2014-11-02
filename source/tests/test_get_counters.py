# coding: utf

from unittest import TestCase
import rstr
import re
from source import lib

class TestGetCounters(TestCase):
    def test_all_counters_detected(self):
        COUNTER_TYPES = (
            ('GOOGLE_ANALYTICS', re.compile(r'.*google-analytics\.com/ga\.js.*', re.I + re.S)),
            ('YA_METRICA', re.compile(r'.*mc\.yandex\.ru/metrika/watch\.js.*', re.I + re.S)),
            ('TOP_MAIL_RU', re.compile(r'.*top-fwz1\.mail\.ru/counter.*', re.I + re.S)),
            ('TOP_MAIL_RU', re.compile(r'.*top\.mail\.ru/jump\?from.*', re.I + re.S)),
            ('DOUBLECLICK',
             re.compile(r'.*//googleads\.g\.doubleclick\.net/pagead/viewthroughconversion.*', re.I + re.S)),
            ('VISUALDNA', re.compile(r'.*//a1\.vdna-assets\.com/analytics\.js.*', re.I + re.S)),
            ('LI_RU', re.compile(r'.*/counter\.yadro\.ru/hit.*', re.I + re.S)),
            ('RAMBLER_TOP100', re.compile(r'.*counter\.rambler\.ru/top100.*', re.I + re.S))
        )
        content = ""
        for counter_name, regexp in COUNTER_TYPES:
            content += rstr.xeger(regexp)

        counters = lib.get_counters(content)

        for counter_name, regexp in COUNTER_TYPES:
            self.assertTrue(counter_name in counters)
        self.assertEqual(len(COUNTER_TYPES), len(counters))

    def test_no_counters_detected(self):
        content = ""
        counters = lib.get_counters(content)
        self.assertEqual([], counters)

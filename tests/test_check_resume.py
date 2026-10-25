import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/resume-tailor/scripts/check_resume.py"
spec = importlib.util.spec_from_file_location("check_resume", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ResumeChecks(unittest.TestCase):
    def test_chinese_and_english_spacing(self):
        self.assertFalse(mod.inspect("使用 AI完成3 个模块")["ok"])

    def test_across_bold_tags(self):
        result = mod.inspect("用**AI** 完成 **3** 个模块")
        self.assertTrue(any(e["kind"] == "spacing" for e in result["errors"]))

    def test_english_names_preserved(self):
        self.assertTrue(mod.inspect("使用Claude Code和Vibe Coding，体验MiniMax H3模型。")["ok"])

    def test_html_and_entities(self):
        self.assertFalse(mod.inspect("完成<strong>3</strong>&nbsp;个模块")["ok"])

    def test_paragraph_budget(self):
        result = mod.inspect("甲\n\n乙\n\n丙\n\n丁\n\n戊")
        self.assertEqual(result["paragraphs"], 5)
        self.assertFalse(result["ok"])

    def test_character_budget(self):
        self.assertFalse(mod.inspect("完成3项", max_chars=3)["ok"])
        self.assertTrue(mod.inspect("完成3项", max_chars=4)["ok"])

    def test_code_and_url_not_linted(self):
        text = "示例`中 AI`与[链接](https://example.test/a%20b)\n\n```python\nx = '中 AI'\n```"
        self.assertTrue(mod.inspect(text)["ok"])

    def test_empty_rejected(self):
        self.assertFalse(mod.inspect(" \n")["ok"])

    def test_cli_read_only_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "experience.txt"
            body = "使用 AI完成测试"
            path.write_text(body, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(path.read_text(encoding="utf-8"), body)
            path.write_text("使用AI完成测试", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()

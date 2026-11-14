import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.version = '0.73.0+example'
        self.platform = 'linux-x64'
        self.install = self.root / 'cache' / 'tessl' / self.version / self.platform
        self.archive = self.root / 'download.tar.gz'
        binary = b'#!/usr/bin/env bash\necho "tessl fixture"\n'
        with tarfile.open(self.archive, 'w:gz') as archive:
            info = tarfile.TarInfo(f'tessl-{self.version}-{self.platform}')
            info.size, info.mode = len(binary), 0o755
            archive.addfile(info, io.BytesIO(binary))
        tools = self.root / 'bin'
        tools.mkdir()
        curl = tools / 'curl'
        curl.write_text('''#!/usr/bin/env python3
import os, pathlib, shutil, sys
with open(os.environ['DOWNLOAD_LOG'], 'a') as log:
    log.write(' '.join(sys.argv[1:]) + '\\n')
shutil.copyfile(os.environ['FIXTURE_ARCHIVE'], sys.argv[sys.argv.index('-o') + 1])
''')
        curl.chmod(0o755)
        self.env = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ['PATH'],
                        VERSION=self.version, PLATFORM=self.platform,
                        RUNNER_TOOL_CACHE=str(self.root / 'cache'),
                        GITHUB_OUTPUT=str(self.root / 'output'),
                        FIXTURE_ARCHIVE=str(self.archive), DOWNLOAD_LOG=str(self.root / 'downloads'))

    def run_install(self):
        action = (ROOT / 'action.yml').read_text()
        block = action.split('    - name: Download and install Tessl CLI', 1)[1]
        block = block.split('      run: |\n', 1)[1].split('\n    - name:', 1)[0]
        script = '\n'.join(line[8:] for line in block.splitlines())
        result = subprocess.run(['bash', '-eo', 'pipefail', '-c', script], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def downloads(self):
        return (self.root / 'downloads').read_text().splitlines()

    def test_reuses_a_verified_installation(self):
        self.run_install()
        self.run_install()
        self.assertEqual(len(self.downloads()), 1)
        self.assertIn('0.73.0%2Bexample', self.downloads()[0])
        self.assertTrue((self.install / 'tessl').is_file())
        self.assertIn(f'binary-path={self.install}/tessl', (self.root / 'output').read_text())

    def test_recovers_when_cached_binary_cannot_run(self):
        self.run_install()
        (self.install / 'tessl').write_text('#!/usr/bin/env bash\nexit 1\n')
        self.run_install()
        self.assertEqual(len(self.downloads()), 2)

    def test_does_not_reuse_an_incomplete_cache_entry(self):
        self.install.mkdir(parents=True)
        binary = self.install / 'tessl'
        binary.write_text('#!/usr/bin/env bash\necho incomplete\n')
        binary.chmod(0o755)
        self.run_install()
        self.assertIn('fixture', subprocess.check_output([str(binary)], text=True))
        self.assertEqual(len(self.downloads()), 1)


if __name__ == '__main__':
    unittest.main()

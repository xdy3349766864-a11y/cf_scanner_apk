name: Build APK
on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip install --upgrade pip
          # 核心修复：锁定旧版 Cython 避免 Python 3.11 编译冲突
          pip install buildozer "Cython<3.0"

      - name: Build with Buildozer
        run: yes | buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: cf-scanner-release
          path: bin/*.apk

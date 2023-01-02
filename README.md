# png2sp
Transparent PNG data to X68k sprite data converter

### Install

    pip install git+https://github.com/tantanGH/png2sp.git

### Usage

    png2sp [options] <input-png-file>

Input movie file can be .mp4 or .avi either.

    options:
        -o [output-file] ... 出力先テキストファイル名 指定しない場合は標準出力
        -f [format]      ... r: unsigned short 配列として出力  b: 1ドットごとの unsigned char 配列として出力
        -x [width]       ... 横サイズ 16の倍数であること
        -y [height]      ... 縦サイズ 16の倍数であること

Note that you need to add mov2gif installed folder to your PATH environment variable.


### Windowsユーザ向けPython導入ガイド

[詳細な日本語での導入ガイド](https://github.com/tantanGH/distribution/blob/main/windows_python_for_x68k.md)
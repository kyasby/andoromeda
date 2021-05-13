# Andoromeda
## 用途
JSONをNGSIに整形してmdgのFIWAREにPOSTするツールです。JSONとNGSIの対応は`settings.yaml`に登録してください。

## 使い方
### インストール
`pip`コマンドでインストールできます。`pip3`であれば下記のように実行します。
```bash
pip3 install -U git+https://github.com/mdg-nu/andromeda.git
```

### Get Started
Pythonスクリプトの冒頭に
```python
import andoromeda
```
と記述します。これでモジュール群が使えるようになります。使い方は`docs`の`Tutorial.md`をご覧ください。

## トラブル・改善
問題がございましたら`issue`にお願いします。
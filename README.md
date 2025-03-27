1. 程序文件结构和安装：
- 主要文件包括：molecular_weight_calculator.py（核心计算逻辑）、app.py（Web服务）、templates/index.html（前端界面）
- 安装步骤：
  a) 确保安装了Python 3.x
  b) 安装依赖包：pip install -r requirements.txt
2. 启动程序：
- 在命令行中进入程序目录
- 运行命令：python app.py
- 在浏览器中访问： http://127.0.0.1:5000
- 注意事项：确保5000端口未被占用
3. 使用说明：
- 在网页界面输入化学分子式（如VOSO4）
- 输入电子转移数、电池电压和溶解度（支持3位小数）
- 点击计算按钮获取结果
- 可以同时输入多个分子式进行批量计算
- 结果将显示分子量分析、存储1kWh所需质量和溶液能量密度

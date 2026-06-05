# 进口牛肉贸易商 WMS 仓储管理系统

## 项目介绍

这是一个为进口牛肉贸易商设计的仓储管理系统(WMS)，用于管理仓库、产品、批次、库存、入出库等业务。

## 主要功能

### 基础设置
- **仓库管理**: 创建和管理仓库信息
- **库区管理**: 管理仓库下的库区
- **产品管理**: 管理产品信息，包括规格、保质期等
- **供应商管理**: 管理供应商信息和原产地

### 批次管理
- **批次录入**: 按批次管理进口牛肉
- **批号生成**: 自动生成批次编号
- **库存跟踪**: 实时追踪各批次库存

### 入出库管理
- **入库操作**: 记录产品入库
- **出库操作**: 记录产品出库
- **库存查询**: 查看实时库存状态
- **库存预警**: 监控即将过期的产品

### 费用管理
- **费用规则**: 定义仓储费、操作费等费用规则
- **费用计算**: 自动计算各类费用
- **费用记录**: 记录所有费用交易
- **费用报表**: 生成费用统计报表

### 数据管理
- **Excel导入**: 批量导入产品、供应商等数据
- **Excel导出**: 导出库存、交易等数据
- **数据验证**: 导入时进行数据验证

## 系统架构

```
├── app.py                    # Flask应用入口
├── config.py                 # 配置文件
├── models/                   # 数据模型
│   ├── warehouse.py
│   ├── storage_area.py
│   ├── product.py
│   ├── supplier.py
│   ├── batch.py
│   ├── inbound.py
│   ├── outbound.py
│   ├── inventory.py
│   ├── fee_rule.py
│   └── fee_record.py
├── routes/                   # 路由处理
│   ├── main.py
│   ├── warehouse.py
│   ├── storage_area.py
│   ├── product.py
│   ├── supplier.py
│   ├── batch.py
│   ├── inbound.py
│   ├── outbound.py
│   ├── inventory.py
│   ├── fee_management.py
│   └── excel_import_export.py
├── services/                 # 业务逻辑
│   ├── auto_code_generator.py
│   └── excel_service.py
├── templates/               # HTML模板
└── requirements.txt         # 依赖清单
```

## 技术栈

- **后端框架**: Flask 2.3.3
- **数据库**: SQLite (开发) / MySQL (生产)
- **ORM**: SQLAlchemy 2.0
- **数据处理**: Pandas, openpyxl
- **前端**: Jinja2 + Bootstrap

## 安装与运行

### 1. 克隆项目
```bash
git clone https://github.com/inja8790/beef-wms.git
cd beef-wms
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 初始化数据库
```bash
python
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
>>>     from models import db
>>>     db.create_all()
```

### 5. 运行应用
```bash
python app.py
```

访问 http://localhost:5000

## 数据库模型

### 主要实体

| 表名 | 描述 |
|------|------|
| warehouse | 仓库信息 |
| storage_area | 库区信息 |
| product | 产品信息 |
| supplier | 供应商信息 |
| batch | 批次信息 |
| inbound | 入库单 |
| outbound | 出库单 |
| inventory | 库存信息 |
| fee_rule | 费用规则 |
| fee_record | 费用记录 |

### 关键字段说明

**Batch(批次表)**
- batch_no: 批次号 (自动生成)
- production_date: 生产日期
- expiry_date: 到期日期 (自动计算)
- quantity: 数量 (支持小数)
- unit_price: 单价
- total_price: 总价 (自动计算)

**Inventory(库存表)**
- current_quantity: 当前库存数量
- unit_price: 单价
- amount: 库存金额 (自动计算)

**FeeRecord(费用记录)**
- fee_type: 费用类型
- quantity: 数量
- amount: 费用金额 (自动计算)

## 编码规则

### 自动编码
- 仓库: WH001, WH002, ...
- 库区: SA001, SA002, ...
- 产品: PRO001, PRO002, ...
- 供应商: SUP001, SUP002, ...
- 批次: SUP-20240105-001
- 入库单: RK20240105-0001
- 出库单: CK20240105-0001

## API 端点

### 仓库管理
- `GET /warehouse/` - 仓库列表
- `POST /warehouse/create` - 创建仓库
- `GET /warehouse/<id>/edit` - 编辑仓库
- `DELETE /warehouse/<id>/delete` - 删除仓库

### 库存管理
- `GET /inventory/` - 库存列表
- `GET /inventory/api/stats` - 库存统计

### 费用管理
- `GET /fee_management/rules` - 费用规则列表
- `GET /fee_management/records` - 费用记录列表

### 数据导入导出
- `GET /excel/templates` - 导入模板
- `POST /excel/import` - 导入数据
- `GET /excel/download-template/<type>` - 下载模板

## 配置说明

编辑 `config.py` 修改配置：

```python
# 开发环境
FLASK_ENV=development
DATABASE_URL=sqlite:///beef_wms.db

# 生产环境
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://user:password@localhost/beef_wms
```

## 常见问题

### 1. 导入Excel文件时出现编码错误
确保Excel文件使用UTF-8编码。

### 2. 库存数量显示异常
检查库存数量的小数位数是否超过3位。

### 3. 批次号生成重复
清空批次表后重新生成，系统会自动递增。

## 开发规范

### 代码风格
- 遵循PEP8规范
- 使用4空格缩进
- 函数和类需要文档注释

### 数据库操作
- 所有数据库操作需要进行异常处理
- 执行DELETE操作前需要确认
- 重要操作需要记录日志

### API响应格式
```json
{
  "status": "success|error",
  "message": "操作消息",
  "data": {}
}
```

## 许可证

MIT License

## 联系方式

- 作者: inja8790
- 邮箱: 502393953@qq.com

## 更新日志

### v1.0.0 (2024-01-05)
- 初始版本发布
- 实现所有核心功能

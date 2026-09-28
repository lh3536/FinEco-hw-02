# HW02-2 数据获取说明（仅限中山大学 CSMAR 授权用户）

请登录 CSMAR，按下表导出 CSV 格式的压缩包，**保持默认 ZIP 文件名、不要解压**，放在 `hw02-2/data/raw/` 中。所有财务报表都选 **年报（12-31）**、**报表类型 A = 合并报表**。

| 放入 `raw/` 的文件（前缀） | 表 | 时间范围 | 字段 |
|---|---|---|---|
| `上市公司基本信息年度表*.zip` | `STK_LISTEDCOINFOANL` | 统计截止日期 2005-12-31—2015-12-31，全部 A 股 | Symbol, ShortName, EndDate, ListedCoID, IndustryNameC, IndustryCodeC, FullName, LISTINGDATE |
| `中国上市公司股权性质文件*.zip` | `EN_EquityNatureAll` | 2005—2015 年末，全部 A 股 | Symbol, ShortName, EndDate, ActualControllerName, ActualControllerNatureID, SharesNature, EquityNature, EquityNatureID |
| `上市公司上市状态变更表*.zip` | `STK_ITEMCHANGE` | 变更日期覆盖 2005—2015 | Symbol, DeclareDate, ChangeDate, ChangedItem, InstitutionID, ValueBefore, ValueAfter, VALUE, ReasonID, Comments |
| `资产负债表221438189*.zip`（主表） | `FS_Combas` | 2004-12-31—2015-12-31，合并报表 | Stkcd, ShortName, Accper, Typrep, A001101000 货币资金, A001000000 资产总计, A002101000 短期借款, A002100000 流动负债合计, A002201000 长期借款, A002000000 负债合计, A003000000 所有者权益合计 |
| `资产负债表220455131*.zip`（仅核对） | `FS_Combas` | 同上 | 与主表相同，但不含 A002101000、A002201000 |
| `利润表*.zip` | `FS_Comins` | 2005-12-31—2015-12-31，合并报表 | Stkcd, ShortName, Accper, Typrep, B002000000 净利润 |

说明：
- Notebook 用文件名前缀定位文件。两份资产负债表用导出编号 `221438189` / `220455131` 区分，如果重新下载得到的编号不同，请把含借款科目的那份重命名为以 `资产负债表221438189` 开头，另一份重命名为以 `资产负债表220455131` 开头（这一份只用于核对。如果没有这一份，可以复制主表并改名，核对单元格同样会通过）。
- 2004 年的资产负债表只用于计算 2005 年的平均总资产和平均权益。
- 请勿公开上传这些文件，以及运行后 `data/processed/`、`outputs/qa/` 中含公司-年记录的文件。

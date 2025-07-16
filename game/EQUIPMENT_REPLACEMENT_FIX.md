# 装备替换修复说明

## 问题描述
用户报告：捡到的装备会自动覆盖之前的装备，导致装备消失。

## 问题原因
在原始的 `equip_item` 方法中，当装备同类型的新装备时：
1. 先调用 `unequip_item` 卸下当前装备，将其放回背包
2. 然后从背包中删除新装备（使用 `player.inventory.pop(inventory_index)`）

但是第一步会在背包中增加一个物品，这可能改变背包中物品的索引，导致第二步删除错误的物品。

## 解决方案
修改 `inventory.py` 中的 `equip_item` 方法：

### 修改前的逻辑：
```python
def equip_item(self, player, equipment, inventory_index):
    # 卸下当前装备（如果有）
    if hasattr(player, 'equipped') and equipment.type in player.equipped:
        if player.equipped[equipment.type]:
            self.unequip_item(player, equipment.type)  # 这会改变背包索引
    
    # 然后删除新装备
    player.inventory.pop(inventory_index)  # 可能删除错误的物品
```

### 修改后的逻辑：
```python
def equip_item(self, player, equipment, inventory_index):
    # 先从背包中移除要装备的物品
    item_to_equip = player.inventory.pop(inventory_index)
    
    # 然后卸下当前装备（如果有）
    if hasattr(player, 'equipped') and equipment.type in player.equipped:
        if player.equipped[equipment.type]:
            self.unequip_item(player, equipment.type)  # 现在安全地放回背包
```

## 修复内容
1. **修改装备逻辑顺序**：先从背包移除要装备的物品，再卸下当前装备
2. **添加错误处理**：如果装备失败，将物品放回背包
3. **统一装备ID**：修复了装备系统中ID不一致的问题

## 测试结果
- ✅ 装备替换正常工作
- ✅ 原装备正确放回背包
- ✅ 不会出现装备消失的问题
- ✅ 支持多种装备类型的替换

## 测试方法
运行以下命令测试装备替换功能：
```bash
python test_equipment_fix.py
```

或者在游戏中：
1. 捡到同类型的装备
2. 装备第一个装备
3. 装备第二个装备
4. 检查背包中是否包含第一个装备

## 其他修复
- 修复了 `chain_mail` -> `chain_armor` 的ID不一致问题
- 修复了 `magic_ring` -> `basic_ring` 的ID不一致问题
- 修复了 `power_amulet` -> `power_ring` 的ID不一致问题

现在装备系统完全正常工作，不会再出现装备消失的问题。

from equipment import EquipmentSystem

equipment = EquipmentSystem.get_all_equipment()
print("装备总数:", len(equipment))

magic_ring = equipment.get('magic_ring')
if magic_ring:
    print("✓ 魔法戒指识别成功")
    print("名称:", magic_ring.name)
    print("等级要求:", magic_ring.level_requirement)
    print("属性:", magic_ring.stats)
else:
    print("✗ 魔法戒指未找到")

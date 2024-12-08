from collections import defaultdict


class BiDirectionalDict:
    def __init__(self):
        # 原始映射：从键到值列表
        self.forward_map: dict[int | str, list[int | str]] = defaultdict(list)
        # 反转映射：从值到键列表
        self.reverse_map: dict[int | str, list[int | str]] = defaultdict(list)

    def add(self, key: int | str, values: list[int | str] | int | str):
        """
        添加或更新一个键和它的值列表。
        :param key: 字符串类型的键
        :param values: 字符串类型的值列表
        """
        if not isinstance(values, list):
            values = [values]

            # 更新原始映射
            self.forward_map[key] += values

            # 更新反转映射
            for value in values:
                self.reverse_map[value].append(key)

    def get_keys_by_value(self, value: int | str):
        """
        通过单个值查找所有关联的键。
        :param value: 要查找的值
        :return: 关联该值的所有键组成的列表
        """
        return self.reverse_map.get(value, [])

    def get_values_by_key(self, key: int | str):
        """
        通过键查找所有关联的值。
        :param key: 要查找的键
        :return: 关联该键的所有值组成的列表
        """
        return self.forward_map.get(key, [])

    def remove_key(self, key: int | str):
        """
        移除一个键及其对应的值，并更新反转映射。
        :param key: 要移除的键
        """
        if key in self.forward_map:
            for value in self.forward_map[key]:
                self.reverse_map[value].remove(key)
                if not self.reverse_map[value]:
                    del self.reverse_map[value]
            del self.forward_map[key]

    def remove_value(self, value: int | str):
        """
        移除一个值及其对应的键，并更新原始映射。
        :param value: 要移除的值
        """
        if value in self.reverse_map:
            for key in self.reverse_map[value]:
                self.forward_map[key].remove(value)
                if not self.forward_map[key]:
                    del self.forward_map[key]
            del self.reverse_map[value]

    def remove(self, key: int | str | None = None, value: int | str | None = None):
        if key and not value:
            self.remove_key(key)
        elif value and not key:
            self.remove_value(value)
        elif key and value:
            self.forward_map[key].remove(value)
            self.reverse_map[value].remove(key)
            if not self.forward_map[key]:
                del self.forward_map[key]
            if not self.reverse_map[value]:
                del self.reverse_map[value]

    def __getitem__(self, key: int | str):
        return self.get_values_by_key(key)
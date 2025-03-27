from typing import Dict, Union, List
import re

# 元素周期表数据（原子量数据）
PERIODIC_TABLE: Dict[str, float] = {
    'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'F': 18.998, 'Ne': 20.180, 'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974, 'S': 32.065,
    'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078, 'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996,
    'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.380, 'Ga': 69.723, 'Ge': 72.640,
    'As': 74.922, 'Se': 78.960, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.620, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.950, 'Tc': 98.000, 'Ru': 101.070, 'Rh': 102.906, 'Pd': 106.420, 'Ag': 107.868, 'Cd': 112.411,
    'In': 114.818, 'Sn': 118.710, 'Sb': 121.760, 'Te': 127.600, 'I': 126.904, 'Xe': 131.293, 'Cs': 132.905, 'Ba': 137.327,
    'La': 138.905, 'Ce': 140.116, 'Pr': 140.908, 'Nd': 144.242, 'Pm': 145.000, 'Sm': 150.360, 'Eu': 151.964, 'Gd': 157.250,
    'Tb': 158.925, 'Dy': 162.500, 'Ho': 164.930, 'Er': 167.259, 'Tm': 168.934, 'Yb': 173.054, 'Lu': 174.967, 'Hf': 178.490,
    'Ta': 180.948, 'W': 183.840, 'Re': 186.207, 'Os': 190.230, 'Ir': 192.217, 'Pt': 195.084, 'Au': 196.967, 'Hg': 200.590,
    'Tl': 204.383, 'Pb': 207.200, 'Bi': 208.980, 'Po': 209.000, 'At': 210.000, 'Rn': 222.000, 'Fr': 223.000, 'Ra': 226.000,
    'Ac': 227.000, 'Th': 232.038, 'Pa': 231.036, 'U': 238.029, 'Np': 237.000, 'Pu': 244.000, 'Am': 243.000, 'Cm': 247.000,
    'Bk': 247.000, 'Cf': 251.000, 'Es': 252.000, 'Fm': 257.000, 'Md': 258.000, 'No': 259.000, 'Lr': 266.000, 'Rf': 267.000,
    'Db': 268.000, 'Sg': 269.000, 'Bh': 270.000, 'Hs': 277.000, 'Mt': 278.000, 'Ds': 281.000, 'Rg': 282.000, 'Cn': 285.000,
    'Nh': 286.000, 'Fl': 289.000, 'Mc': 289.000, 'Lv': 293.000, 'Ts': 294.000, 'Og': 294.000
}

class MolecularWeightCalculator:
    def __init__(self):
        self.periodic_table = PERIODIC_TABLE

    def parse_formula(self, formula: str) -> Dict[str, int]:
        """解析化学分子式，返回元素及其原子数的字典

        Args:
            formula: 化学分子式字符串

        Returns:
            包含元素符号和对应原子数的字典

        Raises:
            ValueError: 当分子式格式不正确时抛出
        """
        if not formula:
            raise ValueError("分子式不能为空")

        # 预处理：处理括号和内部数字
        def process_parentheses(formula: str) -> str:
            while '(' in formula:
                # 找到最内层的括号
                inner = re.search(r'\(([^()]+)\)(\d*)', formula)
                if not inner:
                    raise ValueError("括号不匹配")
                
                content = inner.group(1)
                multiplier = inner.group(2)
                multiplier = int(multiplier) if multiplier else 1
                
                # 将括号内的每个原子数乘以倍数
                expanded = ''
                for match in re.finditer(r'([A-Z][a-z]*)([0-9]*)', content):
                    element = match.group(1)
                    count = match.group(2)
                    count = int(count) if count else 1
                    expanded += f'{element}{count * multiplier}'
                
                # 替换原始字符串中的括号部分
                formula = formula[:inner.start()] + expanded + formula[inner.end():]
            
            return formula

        # 处理括号
        formula = process_parentheses(formula)
        
        # 解析处理后的分子式
        elements: Dict[str, int] = {}
        for match in re.finditer(r'([A-Z][a-z]*)([0-9]*)', formula):
            element = match.group(1)
            count = match.group(2)
            count = int(count) if count else 1
            
            if element not in self.periodic_table:
                raise ValueError(f"未知元素: {element}")
            
            elements[element] = elements.get(element, 0) + count
            
        return elements

    def calculate_weight(self, formula: str) -> float:
        """计算分子量

        Args:
            formula: 化学分子式字符串

        Returns:
            分子量（g/mol）

        Raises:
            ValueError: 当分子式格式不正确或包含未知元素时抛出
        """
        try:
            elements = self.parse_formula(formula)
            total_weight = 0.0
            
            print("元素分析:")
            print(f"{'元素':^4} | {'数量':^6} | {'原子量 (g/mol)':^14} | {'总质量 (g/mol)':^14}")
            print("-" * 50)
            
            for element, count in elements.items():
                atomic_weight = self.periodic_table[element]
                element_total_weight = atomic_weight * count
                total_weight += element_total_weight
                print(f"{element:^4} | {count:^6} | {atomic_weight:^14.3f} | {element_total_weight:^14.3f}")
            
            print("-" * 50)
            print(f"总分子量: {total_weight:.3f} g/mol")
            
            return round(total_weight, 3)
        except Exception as e:
            raise ValueError(f"计算分子量时出错: {str(e)}")

    def calculate_active_material_mass(self, formula: str, electron_transfer: float, voltage: float) -> float:
        """计算存储1kWh电能所需的活性物质质量

        Args:
            formula: 活性物质的化学分子式
            electron_transfer: 电子转移数
            voltage: 电池电压（V）

        Returns:
            存储1kWh电能所需的活性物质质量（g）

        Raises:
            ValueError: 当参数无效或计算出错时抛出
        """
        try:
            # 计算分子量
            molecular_weight = self.calculate_weight(formula)
            
            # 法拉第常数 (C/mol)
            F = 96485
            
            # 1 kWh = 1000 W * 3600 s = 3.6 × 10^6 J
            # 计算所需的物质的量 (mol)
            n = (1000 * 3600) / (electron_transfer * F * voltage)
            
            # 计算质量 (g)
            mass = n * molecular_weight
            
            # 输出计算过程
            print("法拉第常数 (F): 96485 C/mol")
            print("1 kWh = 1000 W × 3600 s = 3.6 × 10^6 J\n")
            
            print("所需物质的量计算:")
            print(f"n = (1000 W × 3600 s) ÷ ({electron_transfer} × 96485 C/mol × {voltage} V)")
            print(f"n = {n:.3f} mol\n")
            
            print("质量计算:")
            print(f"m = n × M = {n:.3f} mol × {molecular_weight:.3f} g/mol")
            print(f"m = {mass:.3f} g")
            
            return round(mass, 3)
        except Exception as e:
            raise ValueError(f"计算活性物质质量时出错: {str(e)}")

    def calculate_solution_energy_density(self, formula: str, electron_transfer: float, voltage: float, solubility: float) -> float:
        """计算溶液的能量密度

        Args:
            formula: 活性物质的化学分子式
            electron_transfer: 电子转移数
            voltage: 电池电压（V）
            solubility: 活性物质的溶解度（mol/L）

        Returns:
            溶液的能量密度（kWh/L）

        Raises:
            ValueError: 当参数无效或计算出错时抛出
        """
        try:
            if solubility <= 0:
                raise ValueError("溶解度必须大于0")
            
            # 法拉第常数 (C/mol)
            F = 96485
            
            # 输出基本参数
            print("基本参数:")
            print(f"活性物质: {formula}")
            print(f"电子转移数: {electron_transfer}")
            print(f"电池电压: {voltage} V")
            print(f"溶解度: {solubility} mol/L")
            print(f"法拉第常数 (F): {F} C/mol")
            print("-" * 50)
            
            # 计算单位体积溶液中活性物质的物质的量（mol/L）
            n_per_liter = solubility
            print("\n单位体积溶液中活性物质的量:")
            print(f"n = {solubility} mol/L")
            
            # 计算单位体积溶液的能量（J/L）
            energy_per_liter = n_per_liter * electron_transfer * F * voltage
            print("\n单位体积溶液的能量计算:")
            print(f"E = n × z × F × U")
            print(f"E = {n_per_liter} mol/L × {electron_transfer} × {F} C/mol × {voltage} V")
            print(f"E = {energy_per_liter:.3f} J/L")
            
            # 转换为kWh/L（1 kWh = 3.6 × 10^6 J）
            print("\n能量单位换算:")
            print("1 kWh = 1000 W × 3600 s = 3.6 × 10^6 J")
            energy_density = energy_per_liter / (3.6 * 10**6)
            print(f"能量密度 = {energy_per_liter:.3f} J/L ÷ (3.6 × 10^6) J/kWh")
            print(f"能量密度 = {energy_density:.3f} kWh/L")
            
            return round(energy_density, 3)
        except Exception as e:
            raise ValueError(f"计算溶液能量密度时出错: {str(e)}")

# 使用示例
def main():
    calculator = MolecularWeightCalculator()
    
    # 测试用例
    test_cases = [
        ('H2O', None, None, None),        # 水
        ('NaCl', None, None, None),       # 氯化钠
        ('H2SO4', None, None, None),      # 硫酸
        ('Ca(OH)2', None, None, None),    # 氢氧化钒
        ('Fe2(SO4)3', None, None, None),   # 硫酸铁
        ('VOSO4', 1, 1.2, 2.0)           # 硫酸氧钒（示例活性物质）
    ]
    
    print("分子量计算器")
    print("-" * 50)
    
    for formula, electron_transfer, voltage, solubility in test_cases:
        try:
            elements = calculator.parse_formula(formula)
            total_weight = 0.0
            
            print(f"\n化学式: {formula}")
            print("-" * 50)
            print("元素分析:")
            print(f"{'元素':^4} | {'数量':^6} | {'原子量 (g/mol)':^14} | {'总质量 (g/mol)':^14}")
            print("-" * 50)
            
            for element, count in elements.items():
                atomic_weight = calculator.periodic_table[element]
                element_total_weight = atomic_weight * count
                total_weight += element_total_weight
                print(f"{element:^4} | {count:^6} | {atomic_weight:^14.3f} | {element_total_weight:^14.3f}")
            
            print("-" * 50)
            print(f"总分子量: {total_weight:.3f} g/mol")
            
            # 如果提供了电子转移数、电压和溶解度，计算活性物质质量和溶液能量密度
            if electron_transfer is not None and voltage is not None and solubility is not None:
                print("\n存储1kWh电能所需质量计算过程:")
                print("-" * 50)
                
                # 显示用户输入参数
                print("用户输入参数:")
                print(f"电子转移数: {electron_transfer}")
                print(f"电池电压: {voltage} V")
                print(f"溶解度: {solubility} mol/L")
                print("-" * 50)
                
                # 计算并显示活性物质质量
                mass = calculator.calculate_active_material_mass(formula, electron_transfer, voltage)
                
                # 计算并显示溶液能量密度
                print("\n溶液能量密度计算:")
                print("-" * 50)
                energy_density = calculator.calculate_solution_energy_density(formula, electron_transfer, voltage, solubility)
                print(f"溶液能量密度: {energy_density} kWh/L")
                print("-" * 50)
            
            print("-" * 50)
        except ValueError as e:
            print(f"{formula}: 错误 - {str(e)}")
            print("-" * 50)
            print("-" * 50)

if __name__ == '__main__':
    main()
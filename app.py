from flask import Flask, render_template, request, jsonify
from molecular_weight_calculator import MolecularWeightCalculator
import io
import sys

app = Flask(__name__)
calculator = MolecularWeightCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        formulas = data.get('formulas', [])
        results = []

        for formula_data in formulas:
            formula = formula_data['formula']
            electron_transfer = formula_data['electron_transfer']
            voltage = formula_data['voltage']
            solubility = formula_data['solubility']

            # 捕获打印输出
            output = io.StringIO()
            sys.stdout = output

            # 计算分子量
            molecular_weight = calculator.calculate_weight(formula)
            calculation_details = output.getvalue()
            output.truncate(0)
            output.seek(0)

            result = {
                'formula': formula,
                'molecular_weight': molecular_weight,
                'calculation_details': calculation_details
            }

            # 如果提供了电子转移数和电压，计算活性物质质量
            if electron_transfer is not None and voltage is not None:
                mass = calculator.calculate_active_material_mass(formula, electron_transfer, voltage)
                result['active_material_mass'] = mass
                calculation_details += f"\n{output.getvalue()}"
                output.truncate(0)
                output.seek(0)

            # 如果提供了溶解度，计算能量密度
            if solubility is not None and electron_transfer is not None and voltage is not None:
                energy_density = calculator.calculate_solution_energy_density(
                    formula, electron_transfer, voltage, solubility)
                result['energy_density'] = energy_density
                calculation_details += f"\n{output.getvalue()}"

            result['calculation_details'] = calculation_details
            results.append(result)

            # 恢复标准输出
            sys.stdout = sys.__stdout__

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
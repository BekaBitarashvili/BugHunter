from flask import Flask, render_template, request, send_file
from fpdf import FPDF

app = Flask(__name__)


class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, 'Bug Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()

    pdf = PDF()
    pdf.add_font('DejaVu', '', 'static/fonts/DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'static/fonts/DejaVuSans-Bold.ttf', uni=True)
    pdf.add_font('DejaVu', 'I', 'static/fonts/DejaVuSans-Oblique.ttf', uni=True)
    pdf.add_page()
    pdf.set_font('DejaVu', '', 14)

    for key, value in data.items():
        pdf.cell(0, 10, txt=f'{key.capitalize()}: {value}', ln=True)

    pdf_output = 'bug_report.pdf'
    pdf.output(pdf_output)

    return send_file(pdf_output, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

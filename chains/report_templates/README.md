# Report Templates

This directory contains report templates for different use cases.

## Available Templates

- **Executive Summary**: High-level overview for management
- **Technical Report**: Detailed technical documentation
- **Full Report**: Complete report with all sections
- **HTML Export**: Web-friendly HTML format

## Usage

```python
from chains.report_generator import ReportGenerator
from chains.chain_analyzer import ChainAnalyzer

# Load a chain
analyzer = ChainAnalyzer()
chain = analyzer.load_chain("my_chain.json")

# Generate report
generator = ReportGenerator()
generator.export_to_markdown(chain, "report.md")
generator.export_to_html(chain, "report.html")
```

## Report Sections

1. **Executive Summary**: Overview for stakeholders
2. **Technical Details**: Full attack chain documentation
3. **Visualization**: Mermaid diagram
4. **Recommendations**: Remediation guidance

## Customization

Reports can be customized by modifying `report_generator.py`:
- Add custom sections
- Modify formatting
- Include additional metadata
- Add custom recommendations



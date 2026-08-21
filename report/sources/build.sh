#!/usr/bin/env bash
# Gera report/Blume_Relatorio_Projeto_Final.docx e, se o LibreOffice estiver
# instalado, uma pré-visualização em PDF com o índice já calculado.
#
#   ./report/sources/build.sh            # figuras + docx + pdf
#   ./report/sources/build.sh --no-pdf   # só o docx
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/report/sources"
TMP="$ROOT/.report-tmp"
PY="$TMP/venv/bin/python"

if [[ ! -x "$PY" ]]; then
  python3 -m venv "$TMP/venv"
  "$TMP/venv/bin/pip" install --quiet python-docx matplotlib
fi

"$PY" "$SRC/figures.py"
"$PY" "$SRC/build_report.py"
"$PY" "$SRC/build_report2.py"

[[ "${1:-}" == "--no-pdf" ]] && exit 0
command -v soffice >/dev/null || { echo "soffice não encontrado; PDF ignorado."; exit 0; }

# O LibreOffice sem interface não recalcula campos ao converter, por isso a
# exportação passa por uma macro que atualiza o índice antes de gravar.
PROFILE="$TMP/lohome/louser"
MACRO_DIR="$PROFILE/user/basic/Standard"
mkdir -p "$MACRO_DIR" "$TMP/pdf" "$TMP/lohome/run"

cat > "$MACRO_DIR/script.xlb" <<'XLB'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE library:library PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "library.dtd">
<library:library xmlns:library="http://openoffice.org/2000/library" library:name="Standard" library:readonly="false" library:passwordprotected="false">
 <library:element library:name="Module1"/>
</library:library>
XLB

cat > "$MACRO_DIR/Module1.xba" <<'XBA'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">Sub UpdateAndExport(inUrl As String, outUrl As String)
    Dim opts(0) As New com.sun.star.beans.PropertyValue
    opts(0).Name = "Hidden"
    opts(0).Value = True

    Dim doc As Object
    doc = StarDesktop.loadComponentFromURL(inUrl, "_blank", 0, opts())
    doc.refresh()

    Dim indexes As Object, i As Integer, pass As Integer
    indexes = doc.getDocumentIndexes()
    ' Duas passagens: a primeira preenche o índice, a segunda corrige os
    ' números de página que a própria paginação do índice deslocou.
    For pass = 1 To 2
        For i = 0 To indexes.getCount() - 1
            indexes.getByIndex(i).update()
        Next i
        doc.refresh()
    Next pass

    Dim save(0) As New com.sun.star.beans.PropertyValue
    save(0).Name = "FilterName"
    save(0).Value = "writer_pdf_Export"
    doc.storeToURL(outUrl, save())
    doc.close(False)
End Sub
</script:module>
XBA

DOCX="file://$ROOT/report/Blume_Relatorio_Projeto_Final.docx"
PDF="file://$TMP/pdf/Blume_Relatorio_Projeto_Final.pdf"

HOME="$TMP/lohome" XDG_RUNTIME_DIR="$TMP/lohome/run" soffice \
  --headless --norestore \
  -env:UserInstallation="file://$PROFILE" \
  "macro:///Standard.Module1.UpdateAndExport(\"$DOCX\",\"$PDF\")" >/dev/null 2>&1

echo "pdf: $TMP/pdf/Blume_Relatorio_Projeto_Final.pdf"

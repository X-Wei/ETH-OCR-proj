<TeXmacs|1.99.5>

<style|<tuple|generic|british>>

<\body>
  <doc-data|<doc-title|Text/Name Extraction from Scanned
  Document>|<doc-author|<\author-data|<author-name|X.WEI>>
    \;
  </author-data>>>

  <section|Method overview>

  The task contains 2 tasks: extract text from scanned image, and extract
  participant names (and maybe more structural infromation in the future)
  from the text. The code/notebook is in this <hlink|git
  repo|https://github.com/X-Wei/ETH-OCR-proj/>.\ 

  <subsection|Text extraction>

  For text extraction, in the spirit of enginnering rather than academic, I
  use <code*|pyocr> (which uses tesseract-ocr in the backend) to do the job.\ 

  With the <code*|pyocr> module, we can not only extract raw text, but also
  extract lineboxes/wordboxes, which contain in additional <strong|position
  information> of the recognized texts.\ 

  <subsection|Name extraction>

  I have tried to process the raw text extracted from
  <samp|<verbatim|pyocr>>, then use <verbatim|langid> to detect language then
  use <verbatim|nltk> for named entity recognition (see <hlink|this
  notebook|https://github.com/X-Wei/ETH-OCR-proj/blob/master/python-OCR-proj.ipynb>),
  but this work out poorly as there lacks the pretrained NER model for
  french/german.\ 

  Then I tried to first identify paragraphs by merging wordboxes returned by
  <verbatim|pyocr>, after some tuning, the paragraph separation work out
  pretty well (see <hlink|here|https://github.com/X-Wei/ETH-OCR-proj/blob/master/paraboxes.jpg>).
  Then I just take the string before the semicolon as participant name. With
  this technique I can extract text as paragraphs, and the participant names
  are correctly extracted. The tuning of paragraph separation can be found in
  <hlink|this notebook|https://github.com/X-Wei/ETH-OCR-proj/blob/master/Paragraph%20extraction.ipynb>.\ 

  <section|Run the code>

  To run the code in <verbatim|text_extract.py>, you have to install
  <verbatim|tesseract>, and install the python module: <verbatim|opencv,
  pyocr, matplotlib, Pillow>.\ 

  After installing these, you should be able to run the code, the ocr step
  taks some time (~ 1min), then the code will output paragraphs of text
  extrated, and ouput the participant names.\ 

  <section|Discussion>

  The ad-hoc solution for participant name extraction works well for the test
  image, but maybe this cannot generalize to all scanned documents, but the
  paragraph separation still gives a track of extracting information. Maybe
  should exploit more of the boxes information, for example: box shape, box
  positon, font size inside box, etc. The box information might help us in
  finding structural elements of the document.\ 

  Another thing to explore is the vertical/horizontal lines in image, with
  these lines maybe we can segment the image into several parts, and
  tesseract might work better on separate parts of the image.
</body>

<\initial>
  <\collection>
    <associate|font-base-size|11>
    <associate|page-medium|paper>
    <associate|page-type|letter>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|1|../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-2|<tuple|1.1|1|../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-3|<tuple|1.2|1|../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-4|<tuple|2|1|../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-5|<tuple|3|1|../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Method
      overview> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <with|par-left|<quote|1tab>|1.1<space|2spc>Text extraction
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>>

      <with|par-left|<quote|1tab>|1.2<space|2spc>Name extraction
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>Run
      the code> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|3<space|2spc>Discussion>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>
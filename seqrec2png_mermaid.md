---
mainfont: Lato-Regular.ttf
monofont: RobotoMono-Regular.ttf
mainfontoptions:
- Scale=1.0
- BoldFont=Lato-Bold.ttf
- ItalicFont=Lato-Italic.ttf
- BoldItalicFont=Lato-BoldItalic.ttf
---

# fasta2png

```{.mermaid theme=neutral height=400 width=1000 format=pdf}
graph TD
    subgraph png2SeqRecord
    sq7(load png into byte array)-->sq8(dill load object)
    sq7-.->sq9(decompress dilled obj)
    sq9-.->sq8
    end
    
    subgraph SeqRecord2png
    sq1(SeqIO FASTA parse)-->sq2(dill dumps SeqRecord)
    sq2-->sq3("find nearest perfect square < len(SeqRecord) == image dimensions")
    sq2-.->sq5(compress dilled obj)
    sq5-.->sq3
    sq3-->sq4(add null bytes to fill up into square image)
    sq4-->sq6(save bytes to png)
    end
```
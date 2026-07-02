# BPE Assignment Notes

## 1. Unicode Character for chr(0)
**Question:** What Unicode character does `chr(0)` return?

**Answer:** It returns the null character, `\0`.

## 2. `__repr__()` vs Printed Representation
**Question:** How does this character’s string representation (`__repr__()`) differ from its printed representation?

**Answer:** `repr()` shows the character in a literal, escaped form, while `print()` displays it more naturally for human reading.

## 3. What Happens When This Character Appears in Text?
**Question:** What happens when this character occurs in text?

**Answer:** It is a control character and is usually not visible when printed. It can affect text processing and may be treated specially by some tools or systems.

## 4. Why Prefer UTF-8 Bytes for Tokenizer Training?
**Question:** Why might it be better to train a tokenizer on UTF-8 encoded bytes rather than UTF-16 or UTF-32?

**Answer:** UTF-16 and 32 seem to use up too many bytes per tokeb especially for more special character being represneted by 3 or 4 bytes.

## 5. Why Function Incorrect
**Question:** Consider the following (incorrect) function, which is intended to decode a UTF-8 byte string into a Unicode string. Why is this function incorrect? Provide an example of an input byte string that yields incorrect results.


**Answer:** hello! 22) \n prints as hello! 22) + newline character.  Function is wrong because we use string instead of repr.

## 6. Give a two-byte sequence that does not decode to any Unicode character(s).

**Answer:** é,  Function is wrong because we decode one byte as a time whereas é might be represented using multiple bytes 


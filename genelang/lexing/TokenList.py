class TokenList(list):
    def __repr__(self):
        names = []
        contents = []
        spans = []

        for token in self:
            names.append(token.pattern.name)
            contents.append(repr(token.content))
            spans.append(f"{token.at_index} -> {token.to_index}")

        names_length = max(map(len, names))
        contents_length = max(map(len, contents))
        spans_length = max(map(len, spans))

        return "\n".join(
            f"{name.ljust(names_length)} : {content.ljust(contents_length)} : {span.ljust(spans_length)}"
            for name, content, span in zip(names, contents, spans)
        )

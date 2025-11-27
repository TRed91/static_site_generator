from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag : str, children : list, props : dict[str, str] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")

        if not self.children or len(self.children) == 0:
            raise ValueError("ParentNode must have children to convert to HTML")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
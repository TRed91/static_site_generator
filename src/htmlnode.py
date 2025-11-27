class HTMLNode:
    def __init__(self, tag : str = None, 
                 value : str = None, 
                 children : list = None, 
                 props : dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        
        html_props = ""
        for key, value in self.props.items():
            html_props += f" {key}=\"{value}\""
        
        return html_props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
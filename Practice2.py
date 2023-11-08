children_list = [child.get_browse_name().to_string() for child in children]
formatted_children = ", ".join([f"ns={node.nodeid.NamespaceIndex};{node.nodeid.IdentifierNumeric}" for node in children_list])
print(formatted_children)

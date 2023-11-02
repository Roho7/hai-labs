tech_ontology = {
    "web-dev": {"related-terms": {"more opportunity", "high-paying", "javascript"}},
    "web3": {"related-terms": {"very high-paying", "cutting edge", "volatile"}},
}

tech_data = {"name": "web3", "tech": "solana", "pay": 300000}


def ontology_fixer(tech, ontology):
    tech_type = tech["name"]
    if tech_type in ontology:
        related_terms = ", ".join(ontology[tech_type]["related-terms"])
        return f"This tech, {tech_type} is related to {related_terms}."
    return "Unknown tech type"


print(ontology_fixer(tech_data, tech_ontology))

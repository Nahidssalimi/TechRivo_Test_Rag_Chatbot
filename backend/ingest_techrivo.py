

import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore



KNOWLEDGE_BASE = [
    {
        "title": "Company Overview",
        "content": (
            "TechRivo is a Portuguese technology company headquartered in Lisbon, Portugal. "
            "The company's registered address is Rua Hermano Neves 18, Piso 3, E 7, Lumiar, 1600-477, Lisbon, Portugal. "
            "TechRivo was founded in 2021 by three entrepreneurs: António Jesus, Rúben Rodrigues, and Patryk Majchrzycki. "
            "Two of the founders are Portuguese and one is Polish. "
            "TechRivo is a specialized technology partner delivering high-performance engineering solutions and intelligent systems "
            "to organizations across Europe and beyond. "
            "The company positions itself at the intersection of technical execution and business strategy, "
            "helping companies build scalable, future-ready technologies that drive long-term success. "
            "TechRivo is a Business Process Outsourcing (BPO) company that started outsourcing in response to custom software development client needs. "
            "The company is part of The Fintech House community in Lisbon."
        ),
        "metadata": {"source": "Company Overview", "type": "company_info"}
    },
    {
        "title": "Mission and Values",
        "content": (
            "TechRivo believes that every business, idea, and software implementation deserves to be done right. "
            "Rather than taking a one-size-fits-all approach, TechRivo emphasizes strategic decision-making, "
            "guiding clients toward implementations that are both practical and future-ready. "
            "The company approaches technology as more than just a service — it is a shared vision rooted in fairness, purpose, and long-term value. "
            "TechRivo embraces one of the 17 United Nations Sustainable Development Goals to Transform the World, "
            "specifically fostering and promoting development-oriented policies that support productive activities, "
            "decent job creation, entrepreneurship, creativity, and innovation. "
            "This goal also includes encouraging the formalization and growth of micro-, small-, and medium-sized enterprises, "
            "which has become core to what TechRivo does. "
            "Flexibility, collaboration, and technical excellence are at the core of every engagement."
        ),
        "metadata": {"source": "Mission and Values", "type": "company_info"}
    },
    {
        "title": "Services Offered",
        "content": (
            "TechRivo offers a comprehensive suite of services designed to drive efficiency and success. "
            "Core services include: "
            "1. Software Development — custom software solutions built to client specifications. "
            "2. Software Consulting — strategic technology consulting tailored to client needs. "
            "3. Technical Outsourcing — leasing of multidisciplinary engineering teams to clients. "
            "4. Project Management — end-to-end project planning and delivery. "
            "5. Mobile App Development — crafting custom mobile solutions for both Android and iOS platforms, "
            "including native apps and complex cross-platform applications. "
            "6. Technical Due Diligence — assessing technical capabilities and identifying gaps. "
            "7. Team Optimization — restructuring and optimizing engineering teams for performance. "
            "8. Strategic Consulting — shaping development roadmaps and launching new tech initiatives. "
            "9. Legacy System Modernization — upgrading outdated systems to modern architectures. "
            "10. Integration Services — connecting systems and APIs for seamless operations. "
            "11. IT Infrastructure Management (DevOps) — managing and optimizing IT infrastructure. "
            "12. Information Security — protecting client systems and data. "
            "TechRivo also provides tools that help clients calculate budgets, set milestones, and compare outsourcing costs versus in-house teams."
        ),
        "metadata": {"source": "Services", "type": "services"}
    },
    {
        "title": "Industry Specializations",
        "content": (
            "TechRivo specializes in tailored technology consulting for the financial services sector, "
            "with a specific emphasis on fintech expertise. "
            "The company has deep experience across multiple industries including: "
            "FinTech — providing technical support and solutions to financial institutions, optimizing operations for success. "
            "HealthTech — delivering solutions in the healthcare space including predictive analytics. "
            "PharmaTech — building predictive models for pharmaceutical consumption and drug forecasting. "
            "Automotive — developing CRM platforms with specific automations for the automotive sector. "
            "The team comes mainly from the banking, financial services, and healthcare industries. "
            "Key technology domains include: AML (Anti-Money Laundering), KYC (Know Your Customer), "
            "HL7, FHIR, EHR, SNOMED CT, HIPAA compliance, Clinical Trials, and DeFi (Decentralized Finance)."
        ),
        "metadata": {"source": "Industry Specializations", "type": "expertise"}
    },
    {
        "title": "Technology Stack and Expertise",
        "content": (
            "TechRivo's team has expertise across a wide range of technologies and frameworks. "
            "Programming Languages: Java, C#, TypeScript, Python. "
            "Frontend: Angular. "
            "Backend: Node.js. "
            "Mobile: Native and cross-platform mobile development for Android and iOS. "
            "Data and AI: Machine Learning, predictive analytics, data automation, Spring AI. "
            "DevOps: IT Infrastructure Management, CI/CD pipelines. "
            "Standards and Compliance: B2MML, HL7, FHIR, EHR, SNOMED CT, HIPAA. "
            "The company stays at the forefront of industry advancements, including AI technologies like Spring AI, "
            "and conducts workshops and knowledge-sharing sessions with clients and development teams."
        ),
        "metadata": {"source": "Technology Stack", "type": "expertise"}
    },
    {
        "title": "Team and Culture",
        "content": (
            "TechRivo is described as a small, highly efficient distributed team. "
            "The company is specialists in three areas of expertise: software development, management, and marketing. "
            "TechRivo is known for its hands-on, results-driven approach, working closely with organizations "
            "to assess technical capabilities, identify gaps, and implement streamlined strategies. "
            "The team is noted for their availability, flexibility, and commitment to client success. "
            "Strong team spirit and a small team size contribute to a responsive and dedicated service experience. "
            "TechRivo fosters a culture of continuous learning and knowledge sharing, "
            "including conducting immersive workshops such as Spring AI exploration sessions with client teams. "
            "Key team members mentioned in client testimonials include Ruben and Patryk, who provide technical consultation calls."
        ),
        "metadata": {"source": "Team and Culture", "type": "company_info"}
    },
    {
        "title": "Pricing and Engagement Model",
        "content": (
            "TechRivo approaches pricing with the same level of customization it brings to its engineering solutions. "
            "Pricing is determined based on the specific services required, project scope, and the complexity of each engagement. "
            "Minimum project size starts at $5,000. "
            "Average hourly rate is between $50 and $99 per hour. "
            "TechRivo offers reasonable pricing tailored for non-profits and startups, emphasizing value through timely delivery and strong communication. "
            "Example engagement: Leasing of a multidisciplinary team composed of 7 hours of a Technical Project Manager, "
            "a Part-Time Full Stack Developer, and 7 hours of a QA Engineer, for €2,000 per week. "
            "The company's customized approach means TechRivo is flexible in cooperation methods, timings, and technologies "
            "to foster a close relationship with all clients. "
            "Because of this close relationship, the company's capacity to onboard new clients is limited, "
            "meaning the service customization level stands out from the competition. "
            "Interested businesses are encouraged to schedule a free consultation with one of TechRivo's specialists."
        ),
        "metadata": {"source": "Pricing", "type": "pricing"}
    },
    {
        "title": "Client Testimonials and Case Studies",
        "content": (
            "TechRivo has a strong track record of client satisfaction. Here are highlights from verified testimonials: "
            "1. Porsche Club Victoria (Andrew Bonwick, Committee Member): "
            "TechRivo's automation solution allowed the client to gather ten times more data, meeting expectations. "
            "They were communicative and transparent throughout the process. "
            "Their availability, flexibility, and commitment to the client's success were impressive. "
            "2. Pharmaceutical MVP (Horizon 2020 Grant): "
            "From an idea to an MVP to predict pharma consumption. "
            "TechRivo helped put the idea on paper and go from a proof of concept to a prototype and then to a Minimum Viable Product. "
            "The predictions of the solution were relevant and precise enough for a business case. "
            "The client was able to use the functioning MVP in their grant application. "
            "3. V&C Fundraising (Financial Consulting): "
            "TechRivo analysed processes and identified how automations could save time and effort to scale the business. "
            "The relationship led to further business partnerships, with TechRivo serving as the technology team for several projects. "
            "4. Automotive CRM Platform: "
            "A CRM platform with specific automations for the Automotive sector faced technical challenges as it gained traction. "
            "Tech calls with Ruben and Patryk from TechRivo provided enough guidance to choose the right path regarding system architecture. "
            "5. Investment Wallet Analysis: "
            "TechRivo enabled the client to save time in analytical tasks and clearly understand their investment wallet's real value. "
            "6. Architecture Optimization: "
            "Thanks to TechRivo's architecture update suggestions, a company's software became inexpensive, scalable, and flexible. "
            "General feedback: Clients consistently praise TechRivo for excellent project management, on-time delivery within budget, "
            "clear communication via Slack, video calls, and Jira, and high-quality products that meet or exceed expectations."
        ),
        "metadata": {"source": "Client Testimonials", "type": "testimonials"}
    },
    {
        "title": "Contact and Location",
        "content": (
            "TechRivo is based in Lisbon, Portugal. "
            "Registered address: Rua Hermano Neves 18, Piso 3, E 7, Lumiar, 1600-477, Lisbon, Portugal. "
            "The company operates as a distributed team across Europe. "
            "TechRivo can be reached through their official website at techrivo.com. "
            "They are active on LinkedIn under the company name TechRivo. "
            "To get started, potential clients can schedule a free consultation session with one of TechRivo's specialists. "
            "TechRivo is a member of The Fintech House community in Lisbon."
        ),
        "metadata": {"source": "Contact Info", "type": "contact"}
    },
    {
        "title": "What Sets TechRivo Apart",
        "content": (
            "TechRivo outshines competition in several key ways: "
            "1. Personalized Attention — a hands-on approach ensures personalized service for each client, "
            "driving tangible results by understanding client goals and challenges. "
            "2. Broad Technical Expertise — ranging from machine learning and API integrations to digital marketing and data automation, "
            "enabling comprehensive and effective solutions. "
            "3. Client-Focused Approach — taking the time to understand specific requirements and providing thoughtful, tailored solutions. "
            "4. Reliable Delivery — consistently delivering high-quality products that meet or exceed expectations, "
            "on time and within budget. "
            "5. Strategic Thinking — not just building software, but guiding clients with architecture suggestions "
            "and strategic roadmaps that make software scalable and cost-effective. "
            "6. Limited Onboarding — because of close client relationships, capacity to onboard new clients is limited, "
            "meaning each client receives a high level of customization that stands out from the competition. "
            "7. Sustainability Commitment — aligned with UN Sustainable Development Goals, promoting entrepreneurship, innovation, "
            "and the growth of small and medium-sized enterprises."
        ),
        "metadata": {"source": "Competitive Advantage", "type": "company_info"}
    }
]


def main():
    print("=" * 60)
    print("  TechRivo Knowledge Base Ingestion")
    print("=" * 60)

    print("\n[1/4] Initializing embedding service...")
    embedder = EmbeddingService()

    print("[2/4] Connecting to ChromaDB...")
    store = VectorStore(collection_name="techrivo_docs")

    current_count = store.get_collection_count()
    print(f"       Current documents in DB: {current_count}")

    if current_count > 0:
        print("       Resetting collection to re-ingest fresh data...")
        store.reset_collection()


    print(f"\n[3/4] Embedding {len(KNOWLEDGE_BASE)} knowledge base entries...")
    documents = []
    for i, entry in enumerate(KNOWLEDGE_BASE):
        print(f"       Embedding: {entry['title']}...")
        embedding = embedder.embed_text(entry["content"])
        if embedding:
            documents.append({
                "content": entry["content"],
                "embedding": embedding,
                "metadata": {
                    **entry["metadata"],
                    "title": entry["title"]
                }
            })
        else:
            print(f"       ❌ Failed to embed: {entry['title']}")


    print(f"\n[4/4] Storing {len(documents)} documents in ChromaDB...")
    added = store.add_documents(documents)

 
    final_count = store.get_collection_count()
    print("\n" + "=" * 60)
    print(f"  ✅ Done! {final_count} documents in knowledge base.")
    print("=" * 60)
    print("\n  Restart your backend (python -m app.main) and test the chatbot!\n")


if __name__ == "__main__":
    main()

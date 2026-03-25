import React from 'react';
import Link from 'next/link';

export default function CaseStudies() {
  return (
    <main>
      <section className="hero" style={{ padding: '4rem 0' }}>
        <div className="container">
          <h1>Projets</h1>
          <p className="hero-tagline">Découvrez quelques exemples de projets réalisés</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Études de cas</h2>
          </div>
          <p className="text-center">
            Voici quelques exemples concrets de projets sur lesquels nous avons travaillé. Pour des raisons de confidentialité, 
            certains détails ont été anonymisés, mais ces cas illustrent parfaitement notre approche et les résultats obtenus.
          </p>

          <div id="ai-research" className="project-highlight" style={{ marginBottom: '3rem' }}>
            <h3>Système Multi-agents pour la Recherche Scientifique</h3>
            <div className="project-content">
              <h4>Le défi</h4>
              <p>
                Une équipe de recherche internationale cherchait à optimiser ses processus d'analyse de littérature scientifique 
                et de rédaction, face à un volume croissant de publications et à des délais de plus en plus courts.
              </p>
              
              <h4>La solution</h4>
              <p>
                Développement d'un système multi-agents (KIN) capable de:
              </p>
              <ul>
                <li>Analyser et synthétiser des articles scientifiques complexes</li>
                <li>Générer des ébauches de documents scientifiques structurés</li>
                <li>Effectuer une veille scientifique ciblée et automatisée</li>
                <li>Proposer des analyses critiques de méthodologies de recherche</li>
              </ul>
              
              <h4>Les résultats</h4>
              <ul>
                <li>Réduction de 60% du temps consacré à la revue de littérature</li>
                <li>Amélioration de la qualité et de la précision des analyses</li>
                <li>Augmentation de 40% de la productivité en termes de publications</li>
                <li>Identification de nouvelles pistes de recherche grâce à l'analyse croisée</li>
              </ul>
            </div>
          </div>

          <div id="international-strategy" className="project-highlight" style={{ marginBottom: '3rem' }}>
            <h3>Stratégie Médico-Scientifique Multi-Pays</h3>
            <div className="project-content">
              <h4>Le défi</h4>
              <p>
                Un laboratoire pharmaceutique souhaitait déployer une stratégie médico-scientifique cohérente pour un nouveau 
                produit dans 10 pays, tout en respectant les spécificités réglementaires et culturelles locales.
              </p>
              
              <h4>La solution</h4>
              <p>
                Élaboration d'une stratégie globale adaptable localement:
              </p>
              <ul>
                <li>Analyse approfondie des environnements réglementaires de chaque pays</li>
                <li>Développement d'un socle commun de messages scientifiques adaptables</li>
                <li>Formation des équipes locales aux spécificités du produit</li>
                <li>Création d'outils de communication scientifique modulables</li>
                <li>Mise en place d'un système de coordination internationale</li>
              </ul>
              
              <h4>Les résultats</h4>
              <ul>
                <li>Lancement réussi et simultané dans les 10 pays cibles</li>
                <li>Cohérence du positionnement scientifique à l'échelle internationale</li>
                <li>Réduction de 30% des coûts de développement des supports</li>
                <li>Augmentation significative de l'engagement des professionnels de santé</li>
              </ul>
            </div>
          </div>

          <div id="kol-network" className="project-highlight" style={{ marginBottom: '3rem' }}>
            <h3>Développement d'un Réseau KOL International</h3>
            <div className="project-content">
              <h4>Le défi</h4>
              <p>
                Une entreprise de biotechnologie cherchait à établir sa crédibilité scientifique et à développer 
                des collaborations avec des experts reconnus dans plusieurs pays européens.
              </p>
              
              <h4>La solution</h4>
              <p>
                Mise en place d'une stratégie complète de gestion de KOL:
              </p>
              <ul>
                <li>Cartographie des leaders d'opinion par pays et par domaine d'expertise</li>
                <li>Développement d'un programme d'engagement scientifique personnalisé</li>
                <li>Organisation de boards scientifiques internationaux</li>
                <li>Facilitation de collaborations pour des publications et présentations</li>
                <li>Création d'une plateforme d'échange scientifique entre experts</li>
              </ul>
              
              <h4>Les résultats</h4>
              <ul>
                <li>Constitution d'un réseau de plus de 50 KOL actifs dans 8 pays</li>
                <li>Publication de 12 articles scientifiques en collaboration</li>
                <li>Organisation de 5 symposiums internationaux</li>
                <li>Renforcement significatif de la crédibilité scientifique de l'entreprise</li>
              </ul>
            </div>
          </div>

          <div id="training-program" className="project-highlight">
            <h3>Programme de Formation Médicale pour Forces de Vente</h3>
            <div className="project-content">
              <h4>Le défi</h4>
              <p>
                Une entreprise pharmaceutique souhaitait améliorer les connaissances scientifiques de ses équipes 
                commerciales pour renforcer leur crédibilité auprès des professionnels de santé.
              </p>
              
              <h4>La solution</h4>
              <p>
                Développement d'un programme de formation complet:
              </p>
              <ul>
                <li>Évaluation initiale des connaissances et des besoins</li>
                <li>Création de modules de formation adaptés à différents niveaux</li>
                <li>Développement d'outils pédagogiques innovants (simulations, cas pratiques)</li>
                <li>Mise en place d'un système d'évaluation continue</li>
                <li>Formation de formateurs internes pour assurer la pérennité</li>
              </ul>
              
              <h4>Les résultats</h4>
              <ul>
                <li>Augmentation de 45% du niveau de connaissances scientifiques</li>
                <li>Amélioration significative de la qualité des échanges avec les médecins</li>
                <li>Augmentation de 25% du temps d'entretien avec les professionnels de santé</li>
                <li>Renforcement de la confiance et de la motivation des équipes</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section section-alt">
        <div className="container">
          <div className="section-title">
            <h2>Votre projet est unique</h2>
          </div>
          <p className="text-center">
            Ces études de cas ne représentent qu'un aperçu des projets sur lesquels nous avons travaillé. Chaque défi est unique 
            et mérite une approche personnalisée. Contactez-nous pour discuter de votre projet spécifique.
          </p>
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/contact" className="button">Prendre rendez-vous</Link>
            <Link href="/services" className="button button-secondary">Découvrir nos services</Link>
          </div>
        </div>
      </section>

      {/* Client-side script for animations */}
      <script dangerouslySetInnerHTML={{
        __html: `
          document.addEventListener('DOMContentLoaded', function() {
            // Add animation to project highlights when they come into view
            const projectHighlights = document.querySelectorAll('.project-highlight');
            
            const observer = new IntersectionObserver((entries) => {
              entries.forEach(entry => {
                if (entry.isIntersecting) {
                  entry.target.style.opacity = 1;
                  entry.target.style.transform = 'translateY(0)';
                }
              });
            }, { threshold: 0.1 });
            
            projectHighlights.forEach(item => {
              item.style.opacity = 0;
              item.style.transform = 'translateY(20px)';
              item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              observer.observe(item);
            });
          });
        `
      }} />
    </main>
  );
}

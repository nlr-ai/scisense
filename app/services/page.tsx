import React from 'react';
import Link from 'next/link';

export default function Services() {
  return (
    <main>
      <section className="hero" style={{ padding: '4rem 0' }}>
        <div className="container">
          <h1>Services</h1>
          <p className="hero-tagline">Des solutions sur mesure pour vos défis scientifiques et médicaux</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Nos Services</h2>
          </div>
          <p className="text-center">
            Forte d'une expertise unique combinant recherche scientifique et stratégie d'entreprise, 
            SciSense offre un accompagnement personnalisé pour transformer vos défis scientifiques en opportunités.
          </p>

          <div id="strategy" className="service-card" style={{ marginBottom: '2rem' }}>
            <h3>Stratégie Médicale Internationale</h3>
            <p>
              Développement et implémentation de stratégies médico-scientifiques adaptées aux spécificités 
              réglementaires et culturelles de différents marchés internationaux.
            </p>
            <ul>
              <li>Analyse des environnements réglementaires locaux</li>
              <li>Adaptation des messages scientifiques aux contextes culturels</li>
              <li>Coordination des équipes médicales internationales</li>
              <li>Harmonisation des stratégies entre les différents pays</li>
              <li>Suivi et évaluation des performances des stratégies déployées</li>
            </ul>
          </div>

          <div id="kol" className="service-card" style={{ marginBottom: '2rem' }}>
            <h3>Gestion de Réseaux KOL</h3>
            <p>
              Création et animation de réseaux d'experts médicaux pour faciliter l'échange de données 
              cliniques et renforcer votre positionnement scientifique.
            </p>
            <ul>
              <li>Identification et cartographie des leaders d'opinion</li>
              <li>Développement de relations professionnelles durables</li>
              <li>Organisation de boards scientifiques et d'échanges d'expertise</li>
              <li>Facilitation de collaborations pour des publications et présentations</li>
              <li>Évaluation de l'impact des activités KOL sur votre positionnement</li>
            </ul>
          </div>

          <div id="ai" className="service-card" style={{ marginBottom: '2rem' }}>
            <h3>IA pour la Recherche Scientifique</h3>
            <p>
              Implémentation de systèmes multi-agents pour l'analyse scientifique et la rédaction, 
              optimisant vos processus de recherche et communication.
            </p>
            <ul>
              <li>Développement de systèmes IA pour l'analyse de littérature scientifique</li>
              <li>Création d'outils d'aide à la rédaction scientifique</li>
              <li>Automatisation de la veille scientifique et concurrentielle</li>
              <li>Formation des équipes à l'utilisation des outils IA</li>
              <li>Intégration de l'IA dans les processus de recherche existants</li>
            </ul>
          </div>

          <div id="communication" className="service-card" style={{ marginBottom: '2rem' }}>
            <h3>Communication Scientifique</h3>
            <p>
              Rédaction et validation de publications, articles scientifiques et supports marketing 
              conformes aux exigences réglementaires internationales.
            </p>
            <ul>
              <li>Rédaction de publications scientifiques et médicales</li>
              <li>Développement de supports de communication pour différentes audiences</li>
              <li>Validation réglementaire des contenus scientifiques</li>
              <li>Vulgarisation de données complexes pour différents publics</li>
              <li>Préparation de présentations pour conférences et congrès</li>
            </ul>
          </div>

          <div id="training" className="service-card" style={{ marginBottom: '2rem' }}>
            <h3>Formation Médicale</h3>
            <p>
              Conception et animation de formations médicales pour les équipes commerciales, 
              marketing et scientifiques, adaptées à différents niveaux d'expertise.
            </p>
            <ul>
              <li>Développement de programmes de formation sur mesure</li>
              <li>Animation de sessions de formation interactives</li>
              <li>Création de supports pédagogiques adaptés</li>
              <li>Évaluation des connaissances et suivi des progrès</li>
              <li>Mise à jour régulière des contenus selon les avancées scientifiques</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section section-alt">
        <div className="container">
          <div className="section-title">
            <h2>Méthodologie</h2>
          </div>
          <div className="about-timeline">
            <div className="timeline-item">
              <div className="timeline-dot"></div>
              <div className="timeline-date">Étape 1</div>
              <div className="timeline-content">
                <h3>Analyse des besoins</h3>
                <p>Compréhension approfondie de vos objectifs, défis et contexte spécifique pour proposer des solutions parfaitement adaptées.</p>
              </div>
            </div>
            
            <div className="timeline-item">
              <div className="timeline-dot"></div>
              <div className="timeline-date">Étape 2</div>
              <div className="timeline-content">
                <h3>Élaboration de la stratégie</h3>
                <p>Développement d'une approche sur mesure combinant expertise scientifique et vision stratégique pour répondre à vos besoins spécifiques.</p>
              </div>
            </div>
            
            <div className="timeline-item">
              <div className="timeline-dot"></div>
              <div className="timeline-date">Étape 3</div>
              <div className="timeline-content">
                <h3>Mise en œuvre</h3>
                <p>Déploiement méthodique des solutions avec un accompagnement constant et des ajustements en fonction des retours.</p>
              </div>
            </div>
            
            <div className="timeline-item">
              <div className="timeline-dot"></div>
              <div className="timeline-date">Étape 4</div>
              <div className="timeline-content">
                <h3>Évaluation et optimisation</h3>
                <p>Mesure des résultats et ajustements continus pour garantir l'atteinte des objectifs et maximiser l'impact.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Prêt à transformer vos défis scientifiques en opportunités?</h2>
          </div>
          <p className="text-center">
            Chaque projet est unique et mérite une approche personnalisée. Contactez-nous pour discuter 
            de vos besoins spécifiques et découvrir comment notre expertise peut vous aider à atteindre vos objectifs.
          </p>
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/contact" className="button">Prendre rendez-vous</Link>
            <Link href="/case-studies" className="button button-secondary">Voir nos projets</Link>
          </div>
        </div>
      </section>

      {/* Client-side script for animations */}
      <script dangerouslySetInnerHTML={{
        __html: `
          document.addEventListener('DOMContentLoaded', function() {
            // Add animation to timeline items when they come into view
            const timelineItems = document.querySelectorAll('.timeline-item');
            
            const observer = new IntersectionObserver((entries) => {
              entries.forEach(entry => {
                if (entry.isIntersecting) {
                  entry.target.style.opacity = 1;
                  entry.target.style.transform = 'translateX(0)';
                }
              });
            }, { threshold: 0.2 });
            
            timelineItems.forEach(item => {
              item.style.opacity = 0;
              item.style.transform = 'translateX(-20px)';
              item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              observer.observe(item);
            });
            
            // Add animation to service cards
            const serviceCards = document.querySelectorAll('.service-card');
            
            const cardObserver = new IntersectionObserver((entries) => {
              entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                  setTimeout(() => {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                  }, index * 100); // Staggered animation
                }
              });
            }, { threshold: 0.1 });
            
            serviceCards.forEach(card => {
              card.style.opacity = 0;
              card.style.transform = 'translateY(20px)';
              card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              cardObserver.observe(card);
            });
          });
        `
      }} />
    </main>
  );
}

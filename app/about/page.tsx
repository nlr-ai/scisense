import React from 'react';
import Link from 'next/link';

export default function About() {
  return (
    <main>
      <section className="hero" style={{ padding: '4rem 0' }}>
        <div className="container">
          <h1>À propos de SciSense</h1>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="about-content">
            <div className="profile-card">
              <div className="profile-image">Logo SciSense</div>
              <div className="profile-info">
                <h1 className="profile-name">SciSense</h1>
                <p className="profile-title">Expertise en Affaires Scientifiques & Médicales</p>
                <p className="profile-bio">Du laboratoire à la stratégie internationale, une approche unique combinant rigueur scientifique et vision stratégique.</p>
                <div className="contact-info" style={{ marginBottom: '1rem' }}>
                  <p><a href="mailto:aurore.inchauspe@scisence.fr">aurore.inchauspe@scisence.fr</a><br />
                  <a href="tel:+33629894916">06.29.89.49.16</a></p>
                </div>
                <div className="social-buttons">
                  <a href="https://www.linkedin.com/in/aurore-inchausp%C3%A9-2493938b/" target="_blank" rel="noopener noreferrer" className="social-button" aria-label="LinkedIn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                  </a>
                  <a href="mailto:aurore.inchauspe@scisence.fr" className="social-button" aria-label="Email">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l10 8.104 10-8.104v11.817h-20z"/>
                    </svg>
                  </a>
                  <a href="tel:+33629894916" className="social-button" aria-label="Phone">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M20 22.621l-3.521-6.795c-.008.004-1.974.97-2.064 1.011-2.24 1.086-6.799-7.82-4.609-8.994l2.083-1.026-3.493-6.817-2.106 1.039c-7.202 3.755 4.233 25.982 11.6 22.615.121-.055 2.102-1.029 2.11-1.033z"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>

            <div className="vision-quote">
              "L'excellence scientifique ne peut avoir un impact significatif que lorsqu'elle est communiquée de manière claire, stratégique et adaptée à ses différentes audiences."
            </div>

            <h2>Notre Approche</h2>
            
            <p>Chez SciSense, nous sommes convaincus que l'excellence scientifique ne peut avoir un impact significatif que lorsqu'elle est communiquée de manière claire, stratégique et adaptée à ses différentes audiences. En tant que passerelle entre le monde de la recherche et celui de la stratégie d'entreprise, nous nous engageons à:</p>

            <ul>
              <li>Maintenir les plus hauts standards de rigueur scientifique</li>
              <li>Développer des stratégies de communication innovantes</li>
              <li>Faciliter la collaboration entre équipes scientifiques et commerciales</li>
              <li>Rendre la science accessible sans en sacrifier la complexité</li>
              <li>Intégrer les dernières avancées technologiques, notamment l'IA, dans les processus scientifiques</li>
            </ul>

            <h2>Notre Expertise</h2>

            <div className="about-timeline">
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2020 - Présent</div>
                <div className="timeline-content">
                  <h3>Chef de Projet Affaires scientifiques et médicales</h3>
                  <p><strong>Boiron Groupe</strong></p>
                  <ul>
                    <li>Élaboration et mise en œuvre de stratégies médico-scientifiques dans 10 pays</li>
                    <li>Développement d'un réseau d'experts médicaux et KOLs</li>
                    <li>Collaboration avec les équipes R&D pour structurer des études cliniques</li>
                    <li>Formation médicale des forces de vente</li>
                    <li>Validation de contenu scientifique conforme aux réglementations internationales</li>
                  </ul>
                </div>
              </div>
              
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2019 - 2020</div>
                <div className="timeline-content">
                  <h3>Assistante Chef de Projet Médico-Marketing</h3>
                  <p><strong>Direction des Relations Professionnelles, Boiron Groupe</strong></p>
                  <ul>
                    <li>Participation à l'élaboration de la stratégie de communication médicale</li>
                    <li>Développement d'outils médico-marketing innovants</li>
                  </ul>
                </div>
              </div>
              
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2015 - 2018</div>
                <div className="timeline-content">
                  <h3>Cadre de Laboratoire – Thèse CIFRE</h3>
                  <p><strong>Sanofi & INSERM U1052</strong></p>
                  <ul>
                    <li>Gestion de projets de recherche sur l'hépatite B</li>
                    <li>Collaboration avec Sanofi pour intégrer des innovations biotechnologiques</li>
                    <li>Renforcement des stratégies de recherche translationnelle</li>
                  </ul>
                </div>
              </div>
            </div>

            <h2>Formation</h2>

            <div className="about-timeline">
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2019 - 2020</div>
                <div className="timeline-content">
                  <h3>Certification "Manager en Biotechnologies" (RNCP niveau 1)</h3>
                  <p><strong>Université Catholique de Lyon</strong></p>
                  <p>Renforcement des compétences en gestion et stratégie appliquées aux sciences de la vie.</p>
                </div>
              </div>
              
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2015 - 2018</div>
                <div className="timeline-content">
                  <h3>Doctorat en Biologie Moléculaire, Intégrative et Cellulaire</h3>
                  <p><strong>Université Claude Bernard Lyon 1</strong></p>
                  <p>Recherche spécialisée dans l'hépatite B en collaboration entre Sanofi et l'INSERM (U1052, CRCL). Travaux ayant conduit à 3 publications scientifiques et plusieurs présentations dans des conférences internationales.</p>
                </div>
              </div>
            </div>

            <h2>Expertise et compétences clés</h2>

            <div className="skill-grid">
              <div className="skill-card medical">
                <div className="skill-icon">🔬</div>
                <h4>Affaires médicales & médico-marketing</h4>
                <ul>
                  <li>Gestion de projets scientifiques internationaux</li>
                  <li>Développement et gestion de réseaux KOL</li>
                  <li>Déploiement de stratégies dans 10 pays</li>
                  <li>Coordination d'équipes internationales</li>
                </ul>
              </div>
              
              <div className="skill-card communication">
                <div className="skill-icon">📝</div>
                <h4>Communication & Rédaction scientifique</h4>
                <ul>
                  <li>Vulgarisation scientifique</li>
                  <li>Présentation efficace des données</li>
                  <li>Veille scientifique et analyse critique</li>
                  <li>Rédaction et validation de publications</li>
                </ul>
              </div>
              
              <div className="skill-card ai">
                <div className="skill-icon">🤖</div>
                <h4>IA & Outils numériques en recherche</h4>
                <ul>
                  <li>Applications de l'IA en recherche</li>
                  <li>Systèmes multi-agents pour l'analyse</li>
                  <li>Outils numériques avancés</li>
                  <li>Technologies innovantes en science</li>
                </ul>
              </div>
              
              <div className="skill-card training">
                <div className="skill-icon">👩‍🏫</div>
                <h4>Formation & Stratégie scientifique</h4>
                <ul>
                  <li>Formation médicale des équipes</li>
                  <li>Accompagnement pluridisciplinaire</li>
                  <li>Pilotage de la veille stratégique</li>
                  <li>Supports pédagogiques adaptés</li>
                </ul>
              </div>
            </div>

            <h2>Projets novateurs</h2>

            <div className="project-highlight">
              <h3>Développement d'IA pour la Science (2023 – Présent)</h3>
              <p>Mise en place d'un système multi-agents (KIN) destiné au secteur de la recherche. Ce système innovant peut rédiger des documents scientifiques et effectuer une lecture critique d'articles, avec plusieurs objectifs:</p>
              <ul>
                <li>Améliorer l'efficacité et la précision des processus de recherche scientifique</li>
                <li>Démocratiser l'accès à la recherche de haute qualité</li>
                <li>Permettre aux scientifiques de se concentrer sur l'innovation et la créativité</li>
                <li>Encourager une collaboration plus étroite entre chercheurs et IA</li>
              </ul>
            </div>

            <h3>Autres projets et engagements</h3>

            <div className="about-timeline">
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">2019 - 2020</div>
                <div className="timeline-content">
                  <h3>Campus Création</h3>
                  <p>Participation à un concours de création d'entreprise innovante, développant des compétences entrepreneuriales et une vision stratégique du marché des biotechnologies.</p>
                </div>
              </div>
              
              <div className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-date">Depuis 2019</div>
                <div className="timeline-content">
                  <h3>Engagement associatif et événementiel</h3>
                  <p>Organisation logistique d'événements associatifs, démontrant ses compétences en gestion de projet et coordination d'équipes en dehors du contexte professionnel.</p>
                </div>
              </div>
            </div>

            <h2>Vision professionnelle</h2>

            <div className="vision-quote">
              "En tant que passerelle entre le monde de la recherche et celui de la stratégie d'entreprise, je m'engage à maintenir les plus hauts standards de rigueur scientifique tout en développant des stratégies de communication innovantes."
            </div>

            <p>Aurore est convaincue que l'excellence scientifique ne peut avoir un impact significatif que lorsqu'elle est communiquée de manière claire, stratégique et adaptée à ses différentes audiences. Elle s'engage à:</p>

            <ul>
              <li>Maintenir les plus hauts standards de rigueur scientifique</li>
              <li>Développer des stratégies de communication innovantes</li>
              <li>Faciliter la collaboration entre équipes scientifiques et commerciales</li>
              <li>Rendre la science accessible sans en sacrifier la complexité</li>
              <li>Intégrer les dernières avancées technologiques, notamment l'IA, dans les processus scientifiques</li>
            </ul>

            <h2>Collaborer avec SciSense</h2>

            <p>Travailler avec SciSense, c'est bénéficier d'une approche qui allie:</p>

            <div className="skill-grid">
              <div className="skill-card">
                <div className="skill-icon">🧠</div>
                <h4>Compréhension scientifique</h4>
                <p>Une compréhension approfondie des enjeux scientifiques et de la recherche de pointe.</p>
              </div>
              
              <div className="skill-card">
                <div className="skill-icon">🔭</div>
                <h4>Vision stratégique</h4>
                <p>Une vision stratégique claire pour transformer la science en avantage concurrentiel.</p>
              </div>
              
              <div className="skill-card">
                <div className="skill-icon">💬</div>
                <h4>Communication exceptionnelle</h4>
                <p>Des compétences en communication exceptionnelles pour tous les publics.</p>
              </div>
              
              <div className="skill-card">
                <div className="skill-icon">👥</div>
                <h4>Leadership d'équipe</h4>
                <p>Une capacité à fédérer des équipes pluridisciplinaires vers un objectif commun.</p>
              </div>
            </div>

            <div className="text-center" style={{ marginTop: '3rem' }}>
              <Link href="/contact" className="button">Discuter de votre projet</Link>
            </div>
          </div>
        </div>
      </section>
      
      <section className="section section-alt">
        <div className="container">
          <div className="section-title">
            <h2>Prêt à collaborer?</h2>
          </div>
          <p className="text-center">Que vous cherchiez à développer une stratégie scientifique internationale, à améliorer votre communication médicale ou à former vos équipes, notre expertise unique est à votre service.</p>
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
            
            // Add animation to skill cards
            const skillCards = document.querySelectorAll('.skill-card');
            
            const skillObserver = new IntersectionObserver((entries) => {
              entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                  setTimeout(() => {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                  }, index * 100); // Staggered animation
                }
              });
            }, { threshold: 0.1 });
            
            skillCards.forEach(card => {
              card.style.opacity = 0;
              card.style.transform = 'translateY(20px)';
              card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              skillObserver.observe(card);
            });
          });
        `
      }} />
    </main>
  );
}

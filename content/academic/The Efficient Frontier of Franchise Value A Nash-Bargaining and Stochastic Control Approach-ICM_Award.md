---
title: "The Efficient Frontier of Franchise Value: A Nash-Bargaining and Stochastic Control Approach"
date: 2026-05-11
description: "Author's 2026 ICM Meritorious Winner Paper"
categories: ["Academic"]
---

> > ##  Introduction
> > > The competition problem highlights a structural pain point in modern sports franchises (based on the situation of  WNBA ): attempting to maximize competitive winning often requires bearing exorbitant payroll burdens and financial downside risks.
> > >
> > > To find the optimal balance between "competitive success" and "financial risk control," we constructed a unified **Profit-Performance Control (PPC) framework**. The core technical breakdown is as follows:
> >>
> > > **Core Modeling Pipeline**
> > >
> >> - **Data Processing & Win Inference:** Abandoning the traditional normal distribution assumption, we applied the Johnson ($S_U$) distribution to accurately fit the heavy-tailed and left-skewed characteristics of Player Efficiency Ratings (PER). Combining Quadratic Synergy with a Logistic function, we non-linearly mapped roster quality to expected wins.
> > > - **Game-Theoretical Compensation Mechanism:** By introducing Marginal Revenue Product (MRP) and the Generalized Nash Bargaining Solution (GNBS), we transformed fixed salaries into an option-like structure of "base salary + team performance bonuses," achieving incentive compatibility and risk-sharing between labor and management.
> > > - **MILP Global Optimization:** To handle complex non-linear revenues (such as ticket and brand-related value), we utilized SOS2 relaxations and McCormick Envelopes to transform the model into a Mixed-Integer Linear Programming (MILP) problem. This ensured the model could stably solve for the Pareto optimal frontier of profit and wins under hard salary cap constraints.
> > > - **Dynamic Pricing & Stress Testing:** Incorporating the Louis-Schmeling paradox and fan Lifetime Value (LTV), we reconstructed the ticket pricing logic. Simultaneously, we utilized Conditional Value at Risk ($CVaR$) to quantify and hedge against extreme tail risks, such as severe injuries to core players and league expansion inflation.
> > >
> > > ** Optimization Results & Strategic Output**
> > >
> > > Under stress testing, the PPC framework demonstrated exceptional robustness: it not only increased expected profit by 60% (from $8.3 million to $13.3 million) but also significantly narrowed the risk exposure to financial losses. Based on the model's output, we provided management with a **"Barbell Roster"** allocation strategy—heavily investing in 2-3 top superstars, filling the depth with highly cost-effective rookies, and strictly avoiding inefficient, mediocre contracts.
> > >
> > > **PS:Thanks to my distinguished teammate: @Bill Leung. Bravo!**
> > 
> > ---
> > 
> > ## Read the Paper 
> > 
> > <div style="margin: 2rem 0; background: var(--entry); padding: 10px; border-radius: 8px; text-align: center; border: 1px solid var(--border);">
> > <iframe 
> > src="https://pub-867ab67c87ea4ab3988d1229f98eeb98.r2.dev/academic/2026_ICM_M_Prize_Paper.pdf#view=FitH" 
> >width="100%" 
> >  height="600px" 
> > style="border: none; border-radius: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
> >  </iframe>
> >  <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.7;">
> >             * If the PDF does not render inline, please use the download button below. <br>
> >     </p>
> >    </div>
> > 
> >    
> >    <p align="center">
> >  <a href="https://pub-867ab67c87ea4ab3988d1229f98eeb98.r2.dev/academic/2026_ICM_M_Prize_Paper.pdf" target="_blank" style="background-color: var(--primary); color: var(--theme); padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block; transition: 0.3s; border: 1px solid var(--primary);">
> >     📥 Download Full Paper (PDF)
> > </a>
> >    </p>
> >    ---
> > 
> >   > **Clarification:** This paper was awarded the Meritorious Winner in the 2026 Interdisciplinary Contest in Modeling (ICM). All methodologies are the intellectual property of the authors. Provided for portfolio viewing only.

---
### 




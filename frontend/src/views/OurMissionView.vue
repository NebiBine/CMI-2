<script setup>
import '../assets/styles/mainStyle.css'
import missionBanner from '../assets/images/ourMissionBanner.png'
</script>

<template>
    <section class="ourMission-page">
        <div class="mission-container">
            <header class="mission-header">
                <figure class="mission-banner-wrap">
                    <img :src="missionBanner" class="mission-banner" alt="Our Mission Banner" />
                </figure>
                <p class="mission-label">Our Mission</p>
                <h1>Helping Cities Make Better Everyday Decisions</h1>
                <p class="mission-intro">
                    CMI exists to help municipalities listen better, prioritize clearly, and act faster.
                    We believe city services improve when decisions are based on real resident needs,
                    transparent processes, and measurable outcomes.
                </p>
            </header>

            <section class="mission-section">
                <h2>Why This Matters</h2>
                <p>
                    City teams are expected to solve complex problems with limited time and resources.
                    Without clear insight, urgent issues can be missed and public trust can decrease.
                    Our mission is to reduce that gap between people and institutions by turning feedback
                    into action.
                </p>
            </section>

            <section class="mission-section">
                <h2>How We Work</h2>
                <p>
                    We collect relevant community input, structure it into useful signals, and support
                    local teams in making decisions that are transparent and accountable. The goal is not
                    more data. The goal is better decisions, delivered faster and explained clearly.
                </p>
            </section>

            <section class="mission-section">
                <h2>Our Principles</h2>
                <ul class="mission-list">
                    <li>
                        <strong>Clarity:</strong>
                        Public decisions should be understandable to everyone.
                    </li>
                    <li>
                        <strong>Inclusion:</strong>
                        Different voices and neighborhoods must be represented.
                    </li>
                    <li>
                        <strong>Responsibility:</strong>
                        Outcomes should be tracked and reported openly.
                    </li>
                    <li>
                        <strong>Practical Impact:</strong>
                        Technology should improve daily life, not add complexity.
                    </li>
                </ul>
            </section>

            <section class="mission-section">
                <h2>Our Commitment</h2>
                <p>
                    We are committed to building tools that support better collaboration between city
                    teams and residents. Every feature we build should help communities feel heard,
                    informed, and confident that progress is measurable.
                </p>
            </section>
        </div>
    </section>
</template>
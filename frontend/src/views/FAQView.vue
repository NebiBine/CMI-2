<script setup>
import '../assets/styles/mainStyle.css'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCircleQuestion } from '@fortawesome/free-regular-svg-icons'

const faqSections = [
    {
        title: 'Account and Access',
        items: [
            {
                question: 'How do I create an account?',
                answer: 'Open the Register page, complete your profile details, and submit the form. After registration, you can log in with your email and password.',
            },
            {
                question: 'I forgot my password. How can I reset it?',
                answer: 'Use the Forgot Password option on the login page. We send a reset link to your registered email so you can choose a new password securely.',
            },
        ],
    },
    {
        title: 'Polls and Participation',
        items: [
            {
                question: 'How are city polls selected and published?',
                answer: 'Municipal teams create polls based on active local priorities. Each poll is reviewed before publication to keep questions clear, relevant, and actionable.',
            },
            {
                question: 'Can I submit more than one response to a poll?',
                answer: 'In most cases, each account can submit one response per poll. This helps keep participation fair and prevents duplicate submissions.',
            },
            {
                question: 'Can I edit my answer after submitting?',
                answer: 'If poll settings allow edits, you can update your response while the poll is still open. Once a poll closes, responses are locked for reporting accuracy.',
            },
        ],
    },
    {
        title: 'Rewards and Points',
        items: [
            {
                question: 'How do I earn reward points?',
                answer: 'Points are earned through eligible actions such as poll participation and other community engagement activities defined by your city program.',
            },
            {
                question: 'Where can I see my point balance and reward history?',
                answer: 'Open your rewards or profile area to view your current balance, recent activity, and available redemption options.',
            },
        ],
    },
    {
        title: 'Data and Privacy',
        items: [
            {
                question: 'What data does CMI collect?',
                answer: 'CMI collects account information, participation data, and interaction logs needed to operate the platform, improve reliability, and generate service insights.',
            },
            {
                question: 'Is my personal information shared with third parties?',
                answer: 'Personal data is handled according to platform and municipal privacy policies. Information is not shared outside approved use cases required for service delivery.',
            },
        ],
    },
    {
        title: 'Support',
        items: [
            {
                question: 'How can I report a technical issue?',
                answer: 'Use the support contact option in the platform and include steps to reproduce the issue, screenshots, and your device/browser details for faster resolution.',
            },
            {
                question: 'Who should I contact for account support?',
                answer: 'For login, profile, or access issues, contact the platform support team through the official support channel listed in your account settings.',
            },
        ],
    },
]
</script>

<template>
    <section class="faq-page">
        <div class="faq-container">
            <header class="faq-header">
                <p class="faq-label">FAQ</p>
                <h1>Frequently Asked Questions</h1>
                <p class="faq-intro">
                    Quick answers to common questions about accounts, polls, rewards, privacy,
                    and support.
                </p>
            </header>

            <section
                v-for="section in faqSections" :key="section.title" class="faq-section">
                <h2>{{ section.title }}</h2>
                <n-collapse accordion>
                    <template #arrow>
                        <n-icon class="faq-icon">
                            <FontAwesomeIcon :icon="faCircleQuestion" />
                        </n-icon>
                    </template>
                    <n-collapse-item
                        v-for="item in section.items" :key="item.question" :title="item.question">
                        <p class="faq-answer">{{ item.answer }}</p>
                    </n-collapse-item>
                </n-collapse>
            </section>
        </div>
    </section>
</template>

<style scoped>

</style>
# Introduction
nutriLab is a web application designed to streamline the process of generating personalized meal plans for patients with conditions like Irritable Bowel Syndrome (IBS), leveraging AI to reduce wait times and improve accessibility. This documentation provides a comprehensive overview of the tech stack, explaining each component's role, setup, and integration, addressing the inefficiencies highlighted in the user's experience of long healthcare delays.

# Tech Stack Overview
The tech stack comprises the following technologies, each chosen for their specific strengths in building a robust, efficient, and scalable application:
Next.js (with App Router): A React-based framework for building server-rendered and statically generated web applications, utilizing the App Router for modern routing and navigation.

Tailwind CSS: A utility-first CSS framework for rapid and consistent styling, integrated with Next.js for front-end development.

shadcn(ui): A UI component library built with Tailwind CSS, accelerating development with pre-designed, reusable components.

tRPC: A type-safe API framework for building efficient and scalable server-side APIs, particularly integrated with Next.js.

Supabase: A database platform providing a PostgreSQL database with additional features like authentication, storage, and RESTful API access.

Clerk: A user management platform for handling authentication and user profiles, ensuring seamless sign-ups and logins.

Python FastAPI: A modern, fast web framework for building APIs, used for AI-related backend tasks.

LangGraph: A framework for building AI agents that can use tools and interact with the environment, crucial for meal plan generation.

LangFuse: A platform for tracking and managing interactions with large language models, aiding in monitoring and improving AI performance.
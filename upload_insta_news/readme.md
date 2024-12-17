# NewsBot: Automated News Posting for Social Media


## Description
NewsBot automates the process of scraping, approving, and posting news content to social media platforms, ensuring your news feed is always fresh and engaging. With Discord integration for admin approval, managing a news page has never been easier.

## Overview
NewsBot is an innovative Python-based automation tool designed to manage news pages on Instagram or any platform that supports image uploads. This project aims to streamline the process of gathering, approving, and posting news content, making it easier for admins to maintain an engaging and up-to-date news feed.

## Features
- **News Scraping**: Automatically scrapes news articles and images from various news websites.
- **Caption Generation**: Writes the headline as a caption on the scraped images.
- **Discord Integration**: *Connects to Discord to send news items to the admin for approval*.
- **Approval Workflow**: Admin can approve or reject news items with a thumbs up or down.
  - **Approved Items**: Moved to the upload folder.
  - **Rejected Items**: Moved to the bin.
- **Automated Posting**: Background task (to be implemented) will pick items from the upload folder and post them to Instagram or any news site.

## Description
NewsBot is designed to automate the tedious process of managing a news page. It scrapes the latest news and images from various sources, adds the headline as a caption, and sends the content to a Discord channel for admin approval. The admin can easily approve or reject the news items with a simple thumbs up or down. Approved items are moved to the upload folder, ready for posting, while rejected items are discarded. The background task, once implemented, will automatically post approved news items to the designated social media platform, ensuring your news feed is always fresh and relevant.

To be implemented:
- Implement the background task for automated posting.
- Add support for more social media platforms.
- Enhance the scraping algorithm to cover more news sources.

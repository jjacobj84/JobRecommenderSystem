# Problem Statement:
   A content based recommendation system which recommend job listings based on professional experience , location and sector.

## How it works?
   ### Architecture
   ![picture](slide/Job_Recommeder_Architecture.jpg)

   This software contains two major components.
   * Offline Preprocessor
   * Online Processor
   
   ### Offline Preprocessor ###
   All preprocessing and data gatthering for content based filtering are done offline and stored in DB for a quicker response while recommending. This software is powered by glassdoor and all contents are obtained from www.glassdoor.com
   Preprocessor consist of following components
   * Job Listing Crawler
      * Given a seed of URLS per location and sector, it crawls to actual Job Listings and gathers more detailed information about the advertisement.
   * Employer Sentiment Analyzer
      * Given location and sector, crawls to gather anonymous user reviews and performs sentiment analysis on them and drops employers below a threshold. 
   * Employer portfolio Crawler
      * Given location and sector, crawls to gather information about various employers and industry information
      
  ### Online Processor ###
  Software presents user with a web interface for entering location, category and professional experience summary and responses with top 10 job listing that matches or best fits user.
  

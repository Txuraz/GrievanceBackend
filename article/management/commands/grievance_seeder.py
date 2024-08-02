import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from article.models import Article
from users.models import User

class Command(BaseCommand):
    help = 'Seed the database with grievance data'

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        grievances = [
            # Negative Sentiment
            {"title": "Delayed Processing of Public Applications", "content": "The processing of public applications has been delayed by several months, causing frustration among citizens who are waiting for essential services.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Corruption in Document Issuance", "content": "There have been multiple reports of corruption and bribery involved in the issuance of official documents. This undermines trust in the government office.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Lack of Proper Maintenance of Public Facilities", "content": "Public facilities such as restrooms and waiting areas are not being properly maintained. This reflects poorly on the office's commitment to public service.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Unresponsive Complaint Handling", "content": "Complaints submitted by citizens are not being addressed in a timely manner. This lack of responsiveness is causing dissatisfaction.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Inadequate Staff Training", "content": "Staff members are not adequately trained to handle queries and provide accurate information. This results in poor service quality.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Unclear Procedure for Filing Complaints", "content": "The procedure for filing complaints is unclear and overly complicated, making it difficult for citizens to get their issues resolved.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Long Waiting Times for Services", "content": "Citizens are experiencing excessively long waiting times for basic services, leading to frustration and loss of productivity.", "author": random.choice(users), "sentiment": "negative"},
            {"title": "Poor Accessibility for Disabled Individuals", "content": "Government offices are not adequately accessible to disabled individuals, which excludes a significant portion of the population from accessing essential services.", "author": random.choice(users), "sentiment": "negative"},

            # Positive Sentiment
            {"title": "Efficient Document Processing", "content": "The recent improvements in document processing have significantly reduced wait times, resulting in a much smoother experience for citizens.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Helpful and Knowledgeable Staff", "content": "The staff at the government office have been particularly helpful and knowledgeable, providing accurate information and assistance with a positive attitude.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Successful Public Awareness Campaign", "content": "The recent public awareness campaign about government services has been very effective in educating citizens and improving engagement.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Improved Online Services", "content": "The enhancements to the online services portal have made accessing and applying for government services much more convenient.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Regular Maintenance of Public Facilities", "content": "Public facilities are now being regularly maintained, which has significantly improved their cleanliness and functionality.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Efficient Complaint Resolution", "content": "Complaints are being addressed more efficiently, and resolutions are provided in a timely manner, leading to increased citizen satisfaction.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Clear Guidelines for Service Procedures", "content": "The guidelines for various service procedures have been made clear and accessible, helping citizens navigate the process with ease.", "author": random.choice(users), "sentiment": "positive"},
            {"title": "Increased Accessibility for Disabled Individuals", "content": "Government offices have improved accessibility features, ensuring that disabled individuals can comfortably access the services they need.", "author": random.choice(users), "sentiment": "positive"},

            # Neutral Sentiment
            {"title": "Upcoming Changes to Service Hours", "content": "There will be changes to service hours starting next month. Please check the updated schedule on the official website.", "author": random.choice(users), "sentiment": "neutral"},
            {"title": "Routine Maintenance Schedule", "content": "Routine maintenance will be conducted on the office's systems over the weekend. Some services may be temporarily unavailable.", "author": random.choice(users), "sentiment": "neutral"},
            {"title": "New Policy Implementation", "content": "A new policy will be implemented starting next week. Citizens are advised to review the policy changes on the official notice board.", "author": random.choice(users), "sentiment": "neutral"},
            {"title": "Annual Report Released", "content": "The annual report of the office has been released and is available for review on the official website. It includes updates and statistics for the past year.", "author": random.choice(users), "sentiment": "neutral"},
            {"title": "Public Survey on Service Satisfaction", "content": "A public survey on service satisfaction will be conducted next month. Citizens are encouraged to provide their feedback to help improve services.", "author": random.choice(users), "sentiment": "neutral"}
        ]

        for grievance_data in grievances:
            author = grievance_data['author']
            Article.objects.create(
                title=grievance_data['title'],
                content=grievance_data['content'],
                author=author,
                author_name=author.name,
                created_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded grievances'))

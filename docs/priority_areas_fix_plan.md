# Plan to Fix Priority Areas Implementation

## Problem Overview
The Priority Areas section is appearing empty because:
1. Data from the GraphQL API is not being properly processed
2. Consistency metrics are not being calculated correctly
3. Analytics system expectations don't match actual data structure

## Implementation Plan

### Phase 1: Data Retrieval Improvements
1. Update GQLQuery.py's BATCH_QUERY to include:
   ```graphql
   userCalendar {
     activeYears
     streak
     totalActiveDays
     submissionCalendar # Currently stringified JSON
     dccBadges {
       timestamp
       badge { name, icon }
     }
   }
   submitStats {
     acSubmissionNum {
       difficulty
       count
       submissions
       # Add timestamp data
       lastSubmissionTime
     }
   }
   ```

### Phase 2: Data Processing Layer
1. Enhance data_formatter.py:
   ```python
   def format_user_calendar_data(data):
       calendar_data = data.get("matchedUser", {}).get("userCalendar", {})
       submission_calendar = json.loads(calendar_data.get("submissionCalendar", "{}"))
       
       return {
           "streak": calendar_data.get("streak", 0),
           "totalActiveDays": calendar_data.get("totalActiveDays", 0),
           "dailySubmissions": submission_calendar,
           "badges": calendar_data.get("dccBadges", [])
       }
   ```

### Phase 3: Analytics System Updates
1. Modify pattern_analyzer.py:
   ```python
   def _analyze_consistency(self):
       calendar_data = self.calendar
       current_streak = calendar_data.get("streak", 0)
       total_active_days = calendar_data.get("totalActiveDays", 0)
       daily_submissions = calendar_data.get("dailySubmissions", {})
       
       # Calculate actual consistency metrics
       monthly_active_days = self._calculate_monthly_active_days(daily_submissions)
       avg_problems_per_active_day = self._calculate_avg_problems_per_day(daily_submissions)
       
       return {
           "current_streak": current_streak,
           "monthly_active_days": monthly_active_days,
           "avg_problems_per_active_day": avg_problems_per_active_day,
           "consistency_level": self._determine_consistency_level(
               current_streak,
               monthly_active_days,
               avg_problems_per_active_day
           )
       }
   ```

2. Update analytics_manager.py's priority detection:
   ```python
   def _identify_priority_areas(self, pattern_analysis, skill_analysis):
       priorities = []
       
       # Check consistency
       consistency = pattern_analysis.get("coding_personality", {}).get("consistency_metrics", {})
       monthly_active_days = consistency.get("monthly_active_days", 0)
       if monthly_active_days < 15:
           priorities.append({
               "area": "Consistency",
               "reason": f"Currently active {monthly_active_days}/30 days. Aim for at least 15 days/month",
               "priority": "high"
           })
       
       # Check problem-solving patterns
       problem_stats = skill_analysis.get("problem_mastery", {}).get("difficulty_stats", {})
       for difficulty, stats in problem_stats.items():
           solved = stats.get("solved", 0)
           total = stats.get("total", 0)
           if total > 0:
               completion_rate = (solved / total) * 100
               if completion_rate < 20:
                   priorities.append({
                       "area": f"{difficulty} Problems",
                       "reason": f"Only completed {round(completion_rate)}% of {difficulty} problems",
                       "priority": "medium"
                   })
       
       return priorities
   ```

### Phase 4: Template Updates
1. Update results.html to handle priority level styling:
   ```html
   {% for area in analysis.summary.priority_areas %}
   <div class="recommendation-item priority-{{ area.priority }} mb-3">
       <h5>{{ area.area }}</h5>
       <p>{{ area.reason }}</p>
       {% if area.priority == "high" %}
       <span class="badge bg-danger">High Priority</span>
       {% elif area.priority == "medium" %}
       <span class="badge bg-warning">Medium Priority</span>
       {% else %}
       <span class="badge bg-info">Low Priority</span>
       {% endif %}
   </div>
   {% endfor %}
   ```

## Implementation Steps
1. Start with Phase 1 changes to GQLQuery.py
2. Implement Phase 2 data formatting improvements
3. Update analytics logic in Phase 3
4. Finally apply template changes in Phase 4
5. Test with various user profiles to ensure priorities are being detected correctly

## Success Metrics
- Priority Areas section should display at least one item for new users
- Consistency priorities should appear for users with < 15 active days per month
- Problem-solving priorities should appear for difficulties with < 20% completion rate
- Each priority should have clear reasoning and actionable improvement suggestions
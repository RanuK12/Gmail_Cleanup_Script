# Gmail Cleanup Script

A simple yet effective Google Apps Script to keep your Gmail inbox clean and organized by automatically removing unwanted emails based on customizable criteria.

## Features

- Automatically removes emails based on Gmail search queries
- Configurable for different categories, labels, and time criteria
- Respects starred emails
- Batch processing to handle large volumes of email
- Detailed logging of operations

## How It Works

By default, the script is configured to remove:
- Emails in the "Promotions" category
- That are in the inbox
- That are NOT starred
- That are older than 1 year

## Installation

1. Open [Google Apps Script](https://script.google.com/)
2. Create a new project
3. Copy and paste the code from the `gmail-cleanup.js` file
4. Save the project with a descriptive name (e.g., "Gmail Cleanup")

## Usage

### Manual Execution

1. Open your Google Apps Script project
2. Select the `runCleanup` function from the dropdown menu
3. Click the play button (▶️) to run the script
4. First time, you'll need to authorize the script to access your Gmail

### Automatic Execution (Scheduled)

1. In your Google Apps Script project, click on the clock icon in the sidebar (⏰)
2. Click "Add Trigger"
3. Configure the trigger:
   - Select the `cleanup` function
   - Choose event source as "Time-driven"
   - Select desired frequency (daily, weekly, etc.)
   - Configure specific time for execution
4. Save the trigger

## Customization

### Modify Search Criteria

Edit the `queryArray` to include your own search queries. Google Apps Script uses the same search syntax as Gmail.

Useful query examples:

```javascript
const queryArray = [
  "category:promotions in:inbox AND -in:starred older_than:",  // Old promotions
  "category:social in:inbox AND -in:starred older_than:",      // Old social
  "label:newsletter older_than:",                              // Old newsletters
  "from:example.com AND -in:starred older_than:",              // Old emails from a specific domain
];
```

### Modify Time Periods

Edit the `delayInfo` array to change the time period for each query:

```javascript
const delayInfo = [
  {index: 0, type: "year", value: 1},   // 1 year for query at position 0
  {index: 1, type: "month", value: 6},  // 6 months for query at position 1
  {index: 2, type: "day", value: 30},   // 30 days for query at position 2
  {index: 3, type: "month", value: 3}   // 3 months for query at position 3
];
```

## Precautions

- **Test First**: Before scheduling automatic runs, execute the script manually to verify it works as expected.
- **Backups**: Consider backing up important emails.
- **Trash**: Emails are moved to trash, not immediately permanently deleted.

## License

MIT — © 2026 Ranuk IT Solutions | ranuk.dev

## Contributions

Contributions are welcome. Feel free to open an issue or submit a pull request.

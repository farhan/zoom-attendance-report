# Zoom Attendance Report Generator

Generate comprehensive Excel attendance reports for recurring Zoom meetings with automated data extraction and analysis.

## Features

- 📊 **Automated Excel Reports**: Generate detailed attendance reports in Excel format
- 🔄 **Recurring Meeting Support**: Track attendance across multiple meeting instances
- ⏱️ **Customizable Attendance Criteria**: Set minimum attendance duration thresholds
- 🌍 **Timezone Support**: Handle different timezones with UTC offset configuration
- 🔐 **OAuth2 Authentication**: Secure API integration with Zoom's OAuth2 system

## Quick Start

### Prerequisites

- Python 3.6.5+
- Paid or ZMP account to access [reports api](https://api-us.zoom.us/v2/report/meetings)
- Access to create Server 2 Server OAuth app

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd zoom-attendance-report

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create `configuration.json` in the project root:

```json
{
  "zoom_account": {
    "account_id": "YOUR_ACCOUNT_ID",
    "client_id": "YOUR_CLIENT_ID", 
    "client_secret": "YOUR_CLIENT_SECRET"
  },
  "meeting": {
    "meeting_id": "YOUR_MEETING_ID",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "minimum_minutes_for_attendance": "5",
    "utc_time_diff_hours": "+0.0"
  }
}
```

### Getting Zoom Credentials

Create a [Server-to-Server OAuth app](https://developers.zoom.us/docs/internal-apps/create/) in Zoom Marketplace and find the following required attributes to place in configuration file.

1. **Account ID**: 
2. **Client ID**:
3. **Client Secret**:
4. **Meeting ID**: Available in Zoom meeting details

### Usage

```bash
python main.py
```

The tool will generate an Excel file with detailed attendance reports for the specified date range.

## Configuration Options

| Field | Description | Example |
|-------|-------------|---------|
| `account_id` | Your Zoom account identifier | `"4eAbksq5TIyE-4eAbks"` |
| `client_id` | OAuth2 client ID from Zoom app | `"wNjOySzzwNjOySzzwNjO"` |
| `client_secret` | OAuth2 client secret from Zoom app | `"xUpQKpeQwTBxUpQKpeQwTBxUpQKpeQwTB"` |
| `meeting_id` | Zoom meeting ID to track | `"82110856856"` |
| `start_date` | Report start date (YYYY-MM-DD) | `"2024-01-01"` |
| `end_date` | Report end date (YYYY-MM-DD) | `"2024-01-31"` |
| `minimum_minutes_for_attendance` | Minimum duration to count as present | `"5"` |
| `utc_time_diff_hours` | Timezone offset from UTC | `"+5.0"` (IST), `"-4.0"` (EST) |

## Use Cases

- **Educational Institutions**: Track student attendance in online classes
- **Corporate Training**: Monitor employee participation in training sessions
- **Healthcare**: Document patient attendance in telemedicine appointments
- **Research**: Analyze meeting engagement patterns and attendance trends

## Troubleshooting

- **Authentication Issues**: Verify your OAuth2 credentials and account permissions
- **Meeting Not Found**: Ensure the meeting ID is correct and accessible
- **Date Range Errors**: Check that start_date is before end_date
- **Timezone Issues**: Verify UTC offset matches your local timezone

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

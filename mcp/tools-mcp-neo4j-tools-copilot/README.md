# Neo4j Report Generator

A comprehensive command-line application that connects to Neo4j and generates detailed analytical reports about event visitors, session attendance patterns, and returning visitor behavior. The application supports multiple types of events and trade conferences.

## Features

### Comprehensive Analytics
- **Visitor Statistics**: Total visitor count and detailed demographic analysis
- **Returning Visitor Tracking**: Advanced analysis of visitors who attended associated events in previous years
- **Session Popularity Analysis**: Top 5 most attended sessions from previous year by returning visitors
- **Session Portfolio**: Complete breakdown of current year sessions with scheduling details
- **Cross-Event Intelligence**: Analysis of visitor movement between associated events

### Supported Event Types
- **Type A Events**: Professional association conferences and trade shows
- **Type B Events**: Technology and digital commerce trade shows

### Report Capabilities
- Professional Markdown-formatted reports with timestamps
- Executive summaries with key performance indicators
- Detailed visitor retention analysis and loyalty metrics
- Session scheduling and venue information
- Strategic insights and data-driven recommendations

## Requirements

- **Python**: 3.8+ (recommended 3.9+)
- **Neo4j**: Database with properly structured event/conference data
- **Dependencies**: See `requirements.txt` for exact versions
  - `neo4j==5.28.2`: Neo4j Python driver
  - `python-dotenv==1.1.1`: Environment variable management

## Installation

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neo4j-show-report-generator
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (see Configuration section)

## Configuration

### Environment Variables Setup

Create a `.env` file in the project root directory with your Neo4j credentials:

```bash
# Neo4j Connection Configuration
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-actual-password
NEO4J_DATABASE=neo4j
```

#### Security Notes
- The `.env` file is automatically excluded from git commits via `.gitignore`
- Never commit credentials to version control
- Use strong, unique passwords for production environments

### Alternative: Direct Environment Variables

If you prefer not to use a `.env` file, set environment variables directly:

#### Windows PowerShell:
```powershell
$env:NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
$env:NEO4J_USERNAME="neo4j"
$env:NEO4J_PASSWORD="your-password"
$env:NEO4J_DATABASE="neo4j"
```

#### Linux/Mac:
```bash
export NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

## Usage

### Option 1: Using the Launcher Script (Recommended)
```bash
# Make the script executable (Linux/Mac)
chmod +x run_report.sh

# Run the application
./run_report.sh
```

### Option 2: Direct Python Execution
```bash
# Activate virtual environment (if using)
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Run the application
python show_report_generator.py
```

### Option 3: Manual Execution
```bash
python3 show_report_generator.py
```

## How the Application Works

### Workflow Overview
1. **Database Connection**: Establishes secure connection to Neo4j using environment credentials
2. **Event Discovery**: Automatically detects available events in the database
3. **User Interaction**: Presents available events and prompts for selection
4. **Data Collection**: Executes optimized Cypher queries to gather comprehensive analytics
5. **Report Generation**: Creates professional Markdown report with insights
6. **File Output**: Saves timestamped report file and displays results in terminal

### Interactive Experience
```bash
Neo4j Report Generator
==================================================
Successfully connected to Neo4j database
Available events:
  1. Event A (event_a)
  2. Event B (event_b)

Enter event name (choose from: event_a, event_b): event_a
Processing data for event_a...
Generating report for event: event_a
Report saved to: event_a_report_20250810_143022.md
```

## Report Sections and Analytics

### Key Metrics Dashboard
- **Total Visitors**: Current year attendance count
- **Returning Visitors**: Cross-year visitor analysis
- **Return Rate**: Percentage calculation of visitor loyalty
- **Cross-Event Movement**: Analysis between different event types

### Advanced Visitor Analysis
- **Section a**: Detailed visitor demographics for current year
- **Section b**: Comprehensive analysis of visitors who attended both current and previous year events
- **Retention Insights**: Deep-dive into audience loyalty patterns

### Session Intelligence
- **Top 5 Sessions**: Most popular sessions from previous year among returning visitors
- **Session Performance**: Attendance metrics with event attribution
- **Content Popularity**: Analysis of session topics and engagement

### Current Year Session Portfolio
- **Complete Session Catalog**: Full breakdown of current year programming
- **Scheduling Details**: Date, time, and venue information
- **Sponsorship Tracking**: Sponsored session identification and sponsor attribution
- **Theatre Distribution**: Venue utilization analysis

### Strategic Insights & Recommendations
- **Audience Retention Analysis**: Data-driven insights on visitor loyalty
- **Cross-Event Opportunities**: Recommendations for audience engagement across events
- **Content Strategy**: Session performance insights for future programming
- **Marketing Intelligence**: Audience behavior patterns for targeted campaigns

## Sample Report Output

### Executive Summary Example
```markdown
# Event A Report

**Generated on:** 2025-08-10 14:30:22

## Executive Summary
This report provides comprehensive analysis of Event A, including 
visitor statistics, returning visitor patterns, and session information.

## Visitor Statistics This Year
**Total Visitors:** 1,874

## Returning Visitor Analysis
- **Same Event (A) Last Year:** 420 visitors
- **Associated Event (B) Last Year:** 132 visitors  
- **Total Returning Visitors:** 552 visitors
- **Returning Visitor Rate:** 29.5%
```

### File Naming Convention
Reports are automatically saved with descriptive timestamps:
```
{event_name}_report_{YYYYMMDD_HHMMSS}.md
```
Examples:
- `event_a_report_20250810_143022.md`
- `event_b_report_20250810_143022.md`

## Database Schema Requirements

The application expects a well-structured Neo4j database with the following components:

### Node Types and Labels
- **`Visitor_this_year`**: Current year event attendees
- **`Visitor_last_year_type_a`**: Previous year Type A event attendees
- **`Visitor_last_year_type_b`**: Previous year Type B event attendees
- **`Sessions_this_year`**: Current year session catalog
- **`Sessions_past_year`**: Previous year session archive

### Essential Node Properties
#### Visitor Nodes:
- `show`: Event identifier (e.g., "event_a", "event_b")
- `BadgeId`: Unique visitor identifier
- `Email`: Contact information for visitor linking

#### Session Nodes:
- `title`: Session name/title
- `show`: Associated event identifier
- `date`: Session date
- `start_time` / `end_time`: Session timing
- `theatre__name`: Venue/room information
- `sponsored_session`: Sponsorship flag
- `sponsored_by`: Sponsor organization

### Critical Relationships
- **`Same_Visitor`**: Links current year visitors to their previous year records
- **`attended_session`**: Connects visitors to sessions they attended

### Data Quality Requirements
- All queries include proper null value filtering with `WHERE field IS NOT NULL`
- Non-null validation for critical fields (event names, session titles, visitor IDs)
- Consistent event identifier naming convention

## Testing & Quality Assurance

### Comprehensive Test Suite

The application includes both unit tests and optional integration tests to ensure reliability and data accuracy.

#### Unit Tests
Comprehensive unit tests with mocked Neo4j interactions:
```bash
# Run all unit tests using the test runner script
./run_tests.sh

# Or execute directly with Python
python test_show_report_generator.py
```

**Test Coverage Areas:**
- Database connection handling and error scenarios
- Environment variable validation and configuration
- Data retrieval methods with various data conditions
- Report generation logic and markdown formatting
- File I/O operations and error handling
- User input validation and edge cases
- Main function workflow and exception handling

#### Integration Tests (Optional)
Real database connectivity tests for production validation:
```bash
# Enable and run integration tests (requires actual Neo4j access)
RUN_INTEGRATION_TESTS=true python test_integration.py
```

**Note**: Integration tests require valid Neo4j credentials and are disabled by default to prevent accidental production database access.

### Test Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt

# Run test suite
./run_tests.sh
```

## Error Handling & Troubleshooting

### Comprehensive Error Management
The application includes robust error handling for common scenarios:

#### Database Connection Issues
- **Connection timeouts**: Automatic retry with informative error messages
- **Authentication failures**: Clear credential validation feedback
- **Network connectivity**: Graceful handling of connection disruptions

#### Configuration Problems
- **Missing environment variables**: Detailed guidance on required settings
- **Invalid credentials**: Secure error messaging without exposing sensitive data
- **Database access permissions**: Clear indication of access control issues

#### Data Quality Issues
- **Invalid event names**: User-friendly validation with available options
- **Missing database nodes**: Graceful handling of incomplete data
- **Query execution errors**: Detailed error reporting for debugging

#### File Operations
- **Disk space limitations**: Proactive checking before report generation
- **File permission issues**: Clear error messages for access problems
- **Directory creation**: Automatic handling of missing directories

### Common Troubleshooting Steps

1. **Verify Environment Variables**:
   ```bash
   # Check if variables are set
   echo $NEO4J_URI
   echo $NEO4J_USERNAME
   # Note: Never echo password in production
   ```

2. **Test Database Connection**:
   ```bash
   # Use Neo4j browser or cypher-shell to verify connectivity
   cypher-shell -a $NEO4J_URI -u $NEO4J_USERNAME
   ```

3. **Validate Database Schema**:
   ```cypher
   # Check for required node types
   MATCH (n) RETURN DISTINCT labels(n) as node_types
   
   # Verify relationship types
   MATCH ()-[r]->() RETURN DISTINCT type(r) as relationships
   ```

4. **Check Data Availability**:
   ```cypher
   # Verify event data exists
   MATCH (v:Visitor_this_year) 
   RETURN DISTINCT v.show as available_events
   ```

## Project Structure

```
neo4j-show-report-generator/
├── show_report_generator.py    # Main application with ShowReportGenerator class
├── requirements.txt            # Python dependencies (neo4j, python-dotenv)
├── .env                       # Environment configuration (create from template)
├── .gitignore                 # Git exclusions (includes .env and report files)
│
├── run_report.sh              # Application launcher script (Linux/Mac)
├── run_tests.sh               # Test execution script
│
├── test_show_report_generator.py  # Comprehensive unit test suite
├── test_integration.py           # Optional integration tests
├── TEST_INFO.md                  # Test documentation and guidelines
│
├── README.md                     # This comprehensive documentation
├── README_APP.md                 # Application-specific details
├── LICENSE                       # License information
│
├── examples/                     # Configuration examples
│   ├── mcp.json.adoc            # MCP configuration example
│   └── mcp-no-env.json.adoc     # Alternative MCP configuration
│
└── *_report_*.md                # Generated reports (git-ignored)
    ├── event_a_report_20250808_100155.md
    └── event_b_report_20250810_143022.md
```

## Dependencies & Requirements

### Core Dependencies
- **`neo4j==5.28.2`**: Official Neo4j Python driver for database connectivity
- **`python-dotenv==1.1.1`**: Environment variable management from `.env` files

### System Requirements
- **Python**: 3.8+ (tested with 3.9, 3.10, 3.11)
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Memory**: Minimum 512MB RAM (recommended 1GB+ for large datasets)
- **Network**: HTTPS access to Neo4j database (port 7687 for Bolt protocol)

### Neo4j Requirements
- **Version**: Neo4j 4.0+ (tested with 4.4, 5.x)
- **Authentication**: Username/password or enterprise authentication
- **Protocols**: Supports Bolt, Bolt+TLS, Neo4j+S connections
- **Permissions**: Read access to visitor and session nodes

## Security Considerations

### Credential Management
- **Environment Variables**: Sensitive data stored in `.env` files (excluded from git)
- **No Hardcoded Credentials**: All authentication data externalized
- **Secure Protocols**: TLS encryption for database connections (`neo4j+s://` URLs)

### Data Privacy
- **Generated Reports**: May contain business-sensitive visitor information
- **Report Files**: Automatically excluded from version control via `.gitignore`
- **Data Retention**: Consider local report file retention policies

### Network Security
- **Connection Encryption**: Uses TLS/SSL for database communication
- **Firewall Considerations**: Ensure Neo4j ports (7687, 7474) are accessible
- **Authentication**: Supports enterprise authentication mechanisms

## Performance Considerations

### Query Optimization
- **Indexed Properties**: Ensure `show` property is indexed on visitor nodes
- **Relationship Indexing**: Index `Same_Visitor` and `attended_session` relationships
- **Memory Usage**: Large datasets may require Neo4j memory tuning

### Scaling Recommendations
- **For Large Datasets (>10K visitors)**:
  - Consider query batching for very large result sets
  - Monitor Neo4j heap memory usage
  - Implement connection pooling for multiple concurrent executions

- **Database Performance**:
  ```cypher
  # Recommended indexes for optimal performance
  CREATE INDEX visitor_show_index FOR (v:Visitor_this_year) ON (v.show)
  CREATE INDEX session_show_index FOR (s:Sessions_this_year) ON (s.show)
  ```

## Development & Contributing

### Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd neo4j-show-report-generator

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install development dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env  # Edit with your credentials

# 5. Run tests
./run_tests.sh
```

### Contributing Guidelines
1. **Code Quality**: Follow PEP 8 Python style guidelines
2. **Testing**: All new features must include comprehensive unit tests
3. **Documentation**: Update README.md for any user-facing changes
4. **Database Validation**: Test all Cypher queries against real data before implementation
5. **Error Handling**: Include proper exception handling and user-friendly error messages

### Code Structure Best Practices
- **Null Filtering**: Always include `WHERE field IS NOT NULL` in Cypher queries
- **Type Hints**: Use Python type hints for better code documentation
- **Error Messages**: Provide clear, actionable error messages for users
- **Resource Cleanup**: Ensure proper Neo4j driver connection cleanup

## License & Support

### License
This project is licensed under the terms specified in the `LICENSE` file. Please review licensing terms before commercial use.

### Support Resources
For issues, questions, or feature requests:

1. **Check Documentation**: Review this README and inline code documentation
2. **Validate Environment**: Ensure all environment variables are correctly configured
3. **Test Database Access**: Verify Neo4j connectivity and required schema exists
4. **Review Test Suite**: Run unit tests to identify configuration issues
5. **Check Dependencies**: Ensure all required packages are installed with correct versions

### Community Guidelines
- **Bug Reports**: Include full error messages, environment details, and reproduction steps
- **Feature Requests**: Provide clear use cases and expected behavior
- **Performance Issues**: Include dataset size and query execution times

---

*Neo4j Report Generator - Professional conference and trade show analytics powered by graph database technology.*
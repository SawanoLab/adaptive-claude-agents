#!/bin/bash
# Token Usage Monitoring Script
# Tracks token usage before and after optimization

set -e

REPORT_DIR=".claude/reports"
METRICS_FILE=".claude/token_metrics.jsonl"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔍 Token Usage Monitoring Tool"
echo "=============================="
echo ""

# Create directories if needed
mkdir -p "$REPORT_DIR"
mkdir -p "$(dirname "$METRICS_FILE")"

# Initialize metrics file if it doesn't exist
if [ ! -f "$METRICS_FILE" ]; then
    echo "# Token usage metrics (JSONL format)" > "$METRICS_FILE"
    echo "📝 Created metrics file: $METRICS_FILE"
fi

# Function to log token usage
log_usage() {
    local task_name="$1"
    local tokens="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    echo "{\"timestamp\":\"$timestamp\",\"task\":\"$task_name\",\"tokens\":$tokens}" >> "$METRICS_FILE"
    echo -e "${GREEN}✅ Logged: $task_name - $tokens tokens${NC}"
}

# Function to estimate tokens from text
estimate_tokens() {
    local text="$1"
    # Rough estimate: 1 token ≈ 4 characters
    local chars=$(echo -n "$text" | wc -c)
    echo $((chars / 4))
}

# Function to estimate tokens from file
estimate_file_tokens() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "0"
        return
    fi
    local bytes=$(wc -c < "$file")
    echo $((bytes / 4))
}

# Check recent reports
echo "📊 Recent Token Usage"
echo "--------------------"

if [ -f "$METRICS_FILE" ]; then
    tail -n 5 "$METRICS_FILE" | while read line; do
        if [[ ! "$line" =~ ^# ]]; then
            task=$(echo "$line" | jq -r '.task' 2>/dev/null || echo "Unknown")
            tokens=$(echo "$line" | jq -r '.tokens' 2>/dev/null || echo "0")
            timestamp=$(echo "$line" | jq -r '.timestamp' 2>/dev/null || echo "Unknown")

            echo "  • $task: $tokens tokens ($timestamp)"
        fi
    done
else
    echo "  No metrics yet"
fi

echo ""

# Calculate statistics
if [ -f "$METRICS_FILE" ]; then
    echo "📈 Statistics"
    echo "-------------"

    total_entries=$(grep -c '^{' "$METRICS_FILE" 2>/dev/null || echo "0")

    if [ "$total_entries" -gt 0 ]; then
        # Calculate average (using awk for floating point)
        avg_tokens=$(grep '^{' "$METRICS_FILE" | \
            jq -r '.tokens' | \
            awk '{ sum += $1; n++ } END { if (n > 0) print int(sum / n); else print 0 }')

        # Calculate total
        total_tokens=$(grep '^{' "$METRICS_FILE" | \
            jq -r '.tokens' | \
            awk '{ sum += $1 } END { print int(sum) }')

        # Find max
        max_tokens=$(grep '^{' "$METRICS_FILE" | \
            jq -r '.tokens' | \
            sort -n | tail -1)

        # Find min
        min_tokens=$(grep '^{' "$METRICS_FILE" | \
            jq -r '.tokens' | \
            sort -n | head -1)

        echo "  Total entries: $total_entries"
        echo "  Average tokens: $avg_tokens"
        echo "  Total tokens: $total_tokens"
        echo "  Max tokens: $max_tokens"
        echo "  Min tokens: $min_tokens"

        # Check if optimization is working
        if [ "$avg_tokens" -lt 20000 ]; then
            echo -e "  ${GREEN}✅ Good! Average is below 20k target${NC}"
        elif [ "$avg_tokens" -lt 50000 ]; then
            echo -e "  ${YELLOW}⚠️  Average is acceptable but can improve${NC}"
        else
            echo -e "  ${RED}❌ Average is high - review token optimization strategies${NC}"
        fi
    else
        echo "  No data yet"
    fi
fi

echo ""

# Check reports directory
echo "📁 Generated Reports"
echo "-------------------"

if [ -d "$REPORT_DIR" ]; then
    report_count=$(find "$REPORT_DIR" -name "*.md" 2>/dev/null | wc -l)

    if [ "$report_count" -gt 0 ]; then
        echo "  Found $report_count report(s)"

        # Show recent reports
        find "$REPORT_DIR" -name "*.md" -type f 2>/dev/null | \
            sort -r | \
            head -5 | \
            while read report; do
                size=$(estimate_file_tokens "$report")
                filename=$(basename "$report")
                echo "    • $filename ($size tokens)"
            done

        # Calculate total report tokens
        total_report_tokens=0
        while read report; do
            tokens=$(estimate_file_tokens "$report")
            total_report_tokens=$((total_report_tokens + tokens))
        done < <(find "$REPORT_DIR" -name "*.md" -type f 2>/dev/null)

        echo ""
        echo "  Total tokens in reports: $total_report_tokens"
        echo -e "  ${GREEN}✅ These tokens were saved from main agent context!${NC}"
    else
        echo "  No reports yet"
    fi
else
    echo "  Directory not created yet"
fi

echo ""
echo "💡 Tips:"
echo "  - Target: <20,000 tokens per subagent task"
echo "  - Reports should be <500 tokens (summaries only)"
echo "  - Detailed analysis saved to .claude/reports/"
echo ""
echo "📖 See docs/TOKEN_OPTIMIZATION_GUIDE.md for best practices"

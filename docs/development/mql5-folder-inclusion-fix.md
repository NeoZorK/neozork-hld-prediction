# MQL5 Folder Inclusion Fix

## Problem Description

When users tried to load EURUSD data with "3 eurusd", the system returned "No files found matching mask 'eurusd' in data/indicators/json" because the EURUSD file is located in the `mql5_feed` folder, which was not included in the list of available folders.

### Issue Details

- **Root Cause**: `mql5_feed` folder was not included in the folder discovery logic
- **Symptom**: "❌ No files found matching mask 'eurusd' in data/indicators/json"
- **Expected**: Load `CSVExport_EURUSD_PERIOD_D1.csv` from `mql5_feed/`
- **Actual**: Searched in `data/indicators/json` (folder #3) where no EURUSD files exist

### File Location

```
./mql5_feed/CSVExport_EURUSD_PERIOD_D1.csv  ← EURUSD file location
./data/indicators/json/                      ← Previously searched location
```

## Solution Implementation

### 1. Enhanced Folder Discovery

Modified the folder discovery logic to include the `mql5_feed` folder:

```python
# Get all subfolders in data directory and other important folders
data_folder = Path("data")
mql5_feed_folder = Path("mql5_feed")

if not data_folder.exists():
    print("❌ Data folder not found. Please ensure 'data' folder exists.")
    return False

# Find all subfolders (exclude cache folders)
subfolders = [data_folder]  # Include main data folder

# Add mql5_feed folder if it exists
if mql5_feed_folder.exists() and mql5_feed_folder.is_dir():
    subfolders.append(mql5_feed_folder)
```

### 2. Updated Folder Structure

The new folder structure includes:

```
Available folders:
0. 🔙 Back to Main Menu
1. 📁 data/
2. 📁 mql5_feed/          ← NEW: Added to available folders
3. 📁 data/indicators/
4. 📁 data/indicators/json/
5. 📁 data/indicators/csv/
6. 📁 data/indicators/parquet/
7. 📁 data/raw_parquet/
8. 📁 data/backups/
```

## Testing

### Test Cases Created

1. **`test_mql5_feed_folder_included`**: Verifies mql5_feed folder is in available folders
2. **`test_eurusd_file_found_in_mql5_feed`**: Tests EURUSD file discovery in mql5_feed
3. **`test_folder_number_mapping`**: Validates correct folder number mapping

### Test Results

```bash
✅ Test passed: mql5_feed folder is included in available folders
Found EURUSD files: ['CSVExport_EURUSD_PERIOD_D1.csv']
✅ Test passed: Found 1 EURUSD files
✅ Test passed: mql5_feed folder is at position 2
   Available folders: ['data', 'mql5_feed', 'data/indicators', ...]
```

## Usage

### Before Fix
```bash
./interactive_system.py
# Menu Load Data -> "3 eurusd"
❌ No files found matching mask 'eurusd' in data/indicators/json
```

### After Fix
```bash
./interactive_system.py
# Menu Load Data -> "2 eurusd"  ← Use folder #2 (mql5_feed)
✅ Found 1 data files:
   1. CSVExport_EURUSD_PERIOD_D1.csv (1.4MB)
```

### Correct Folder Numbers

| Folder | Number | Description |
|--------|--------|-------------|
| data/ | 1 | Main data folder |
| **mql5_feed/** | **2** | **MQL5 export files (EURUSD, etc.)** |
| data/indicators/ | 3 | Indicators folder |
| data/indicators/json/ | 4 | JSON indicators |
| data/indicators/csv/ | 5 | CSV indicators |
| data/indicators/parquet/ | 6 | Parquet indicators |
| data/raw_parquet/ | 7 | Raw parquet files |
| data/backups/ | 8 | Backup files |

## Files Modified

1. **`src/interactive/data_manager.py`**:
   - Updated `load_data()` method to include mql5_feed folder
   - Enhanced folder discovery logic
   - Maintained cache exclusion functionality

2. **`tests/interactive/test_data_manager_mql5_fix.py`**:
   - Created comprehensive test suite
   - Tests mql5_feed folder inclusion
   - Tests EURUSD file discovery
   - Validates folder number mapping

## Impact

### Positive Changes
- ✅ **EURUSD file accessible**: Now can load EURUSD data correctly
- ✅ **Better user experience**: Clear folder structure with mql5_feed included
- ✅ **Consistent behavior**: All MQL5 export files now accessible
- ✅ **Backward compatibility**: Existing functionality preserved

### User Instructions

**To load EURUSD data:**
```bash
./interactive_system.py
# Menu Load Data -> "2 eurusd"
```

**To load other MQL5 files:**
```bash
# GBPUSD: "2 gbpusd"
# Any MQL5 file: "2 [filename_pattern]"
```

## Compatibility

The fix maintains backward compatibility with:
- All existing data folder functionality
- Cache exclusion logic
- Temporary file filtering
- Mask filtering functionality

## Future Enhancements

1. **Dynamic folder discovery**: Automatically detect and include other data folders
2. **Folder aliases**: Allow users to use folder names instead of numbers
3. **Smart suggestions**: Suggest correct folder numbers based on file patterns
4. **Folder descriptions**: Add descriptions for each folder in the menu

## Troubleshooting

### If Still Can't Find Files

1. **Check folder number**: Use "2 eurusd" (not "3 eurusd")
2. **Verify file exists**: Ensure `mql5_feed/CSVExport_EURUSD_PERIOD_D1.csv` exists
3. **Check permissions**: Ensure read access to mql5_feed folder
4. **Use direct path**: Try "mql5_feed eurusd" as alternative

### Debug Information

To see available folders and their numbers:
```python
# The system will show:
print("💡 Available folders:")
for i, folder in enumerate(subfolders, 1):
    print(f"{i}. 📁 {folder}/")
```

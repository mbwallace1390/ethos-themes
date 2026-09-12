-- America 250
-- America 250 anniversary theme. Native ETHOS radio theme; no background tasks.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

local function init()
    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
    system.registerTheme({
        key = "USA250",
        name = "America 250",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF0, 0xE7, 0xCF), -- PRIMARY_COLOR
            lcd.RGB(0x1B, 0x2F, 0x48), -- SECONDARY_BGCOLOR
            lcd.RGB(0xD8, 0xAA, 0x4E), -- HIGHLIGHT_COLOR
            lcd.RGB(0x04, 0x0E, 0x1F), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6D, 0x7C, 0x8E), -- DISABLE_COLOR
            lcd.RGB(0x08, 0x18, 0x2F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xBB, 0xCF, 0xE3), -- SECONDARY_COLOR
            lcd.RGB(0x57, 0xDD, 0x90), -- SAFE_COLOR
            lcd.RGB(0x04, 0x0E, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x60, 0x6A), -- ERROR_COLOR
            lcd.RGB(0x7A, 0xB6, 0xF1), -- ACTIVE_COLOR
            lcd.RGB(0x85, 0x97, 0xAA), -- INACTIVE_COLOR
            lcd.RGB(0xD8, 0xAA, 0x4E), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3B, 0x4F, 0x67), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC6, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x08, 0x1C, 0x12), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x04, 0x0E, 0x1F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-america250.png", "toolbar-america250-x18.png"),
    })
end

return { init = init }

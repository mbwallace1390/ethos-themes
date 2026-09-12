-- Blue Resolve
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
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
        key = "BluRsv",
        name = "Blue Resolve",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1D, 0x3E, 0x56), -- SECONDARY_BGCOLOR
            lcd.RGB(0x7E, 0xC8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x79, 0x86, 0x91), -- DISABLE_COLOR
            lcd.RGB(0x13, 0x29, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xBF, 0xE2, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x09, 0x13, 0x1C), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xD3, 0xEE, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x9B, 0xA6, 0xAE), -- INACTIVE_COLOR
            lcd.RGB(0xD3, 0xEE, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x35, 0x66, 0x85), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x09, 0x13, 0x1C), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-blue-resolve.png", "toolbar-blue-resolve-x18.png"),
    })
end

return { init = init }

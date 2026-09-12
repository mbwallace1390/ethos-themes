-- OLED Red
-- Lightweight standalone ETHOS theme.
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
        key = "OLRed",
        name = "OLED Red",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x16, 0x0F, 0x10), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- HIGHLIGHT_COLOR
            lcd.RGB(0x22, 0x22, 0x23), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5B, 0x61, 0x68), -- DISABLE_COLOR
            lcd.RGB(0x0B, 0x08, 0x08), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xA2, 0xAD), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- ACTIVE_COLOR
            lcd.RGB(0x7C, 0x7C, 0x7C), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3A, 0x38, 0x38), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-oled-red.png", "toolbar-oled-red-x18.png"),
    })
end

return { init = init }

-- Gunmetal
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
        key = "Gunmet",
        name = "Gunmetal",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x30, 0x38, 0x40), -- SECONDARY_BGCOLOR
            lcd.RGB(0x7A, 0xA7, 0xC7), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7D, 0x80, 0x85), -- DISABLE_COLOR
            lcd.RGB(0x22, 0x28, 0x2E), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xBC, 0xD2, 0xE3), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x16, 0x1B, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x7A, 0xA7, 0xC7), -- ACTIVE_COLOR
            lcd.RGB(0x9C, 0xA0, 0xA3), -- INACTIVE_COLOR
            lcd.RGB(0x86, 0xAF, 0xCC), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x56, 0x5B), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x16, 0x1B, 0x1F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-gunmetal.png", "toolbar-gunmetal-x18.png"),
    })
end

return { init = init }

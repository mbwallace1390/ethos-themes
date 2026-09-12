-- Blue Vector
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
        key = "BluVec",
        name = "Blue Vector",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x23, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x20, 0x8B, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x09, 0x0F, 0x14), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x6C, 0x72), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x17, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x8F, 0xC3, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0C, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x43, 0xE9, 0x7B), -- ACTIVE_COLOR
            lcd.RGB(0x85, 0x89, 0x8E), -- INACTIVE_COLOR
            lcd.RGB(0x43, 0xE9, 0x7B), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x45, 0x4B, 0x51), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x0C, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-blue-vector.png", "toolbar-blue-vector-x18.png"),
    })
end

return { init = init }

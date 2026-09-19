-- Ember Signal
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
    -- Load the optional palette-matched logo once; failures keep the theme usable.
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-ember-signal.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "EmbSig",
        name = "Ember Signal",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x2E, 0x25, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x8A, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x14, 0x0F, 0x09), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x72, 0x6F, 0x6B), -- DISABLE_COLOR
            lcd.RGB(0x1F, 0x18, 0x10), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xC3, 0x82), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x11, 0x0D, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x4A, 0x3F), -- ACTIVE_COLOR
            lcd.RGB(0x8F, 0x8C, 0x8A), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3B, 0x30), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x4B, 0x46), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x0D, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-ember-signal.png", "toolbar-ember-signal-x18.png"),
    })
end

return { init = init }

module.exports = function(grunt) {

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        clean: {
            all: ['.build/*']
        },
        replace: {
            spec: {
                options: {
                    usePrefix: false,
                    patterns: [{
                            match: /%\s*(.*)/g,
                            replacement: ''
                        },
                        {
                            match: /{{(.*)}}/g,
                            replacement: '{{@@include(\'$1\')}}'
                        },
                        {
                            match: '<CODE BEGINS>',
                            replacement: ''
                        },
                        {
                            match: '<CODE ENDS>',
                            replacement: ''
                        },
                        {
                            match: '{mainmatter}',
                            replacement: ''
                        },
                        {
                            match: '{backmatter}',
                            replacement: ''
                        },
                        {
                            match: '.# Abstract',
                            replacement: ''
                        },
                        {
                            match: ' {#pattern-based-subscriptions}',
                            replacement: ''
                        },
                        {
                            match: ' {#uris}',
                            replacement: ''
                        },
                        {
                            match: ' {#protocol_errors}',
                            replacement: ''
                        }
                    ]
                },
                files: [
                    { expand: true, flatten: false, src: ['rfc/**/*.md'], dest: '.build/' }
                ]
            },
            dev: {
                options: {
                    usePrefix: false,
                    patterns: [{
                        match: '<script src="//localhost:35729/livereload.js"></script>',
                        replacement: ''
                    }]
                },
                files: [
                    { src: 'rfc/aux/footer.html', dest: '.build/footer.html' }
                ]
            }
        },
        includereplace: {
            spec: {
                options: {
                    prefix: '{{@@',
                    suffix: '}}',
                    includesDir: '.build/'
                },
                files: [{
                    expand: true,
                    flatten: true,
                    src: ['.build/rfc/wamp.md'],
                    dest: '.build/'
                }]
            }
        },
        copy: {
            spec: {
                options: {
                    process: (content, srcpath) => {
                        return content
                            .replace(/{align="left"}\n(\s+,((.|\n)*?)')\n\n/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n(\s+\+((.|\n)*?)\+)\n\n/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n(\|(.|\n)*?)(?=\n\n)/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n((.|\n)*?)(?=\n\n[^\s])/gm, '```\n$1\n```\n\n')
                            .replace(/```\n```/g, '```')
                            .replace(/\n\n\n\n/gm, '\n\n');
                    }
                },
                files: [
                    { src: '.build/wamp.md', dest: '.build/wamp-processed.md' }
                ]
            }
        },
        concat: {
            concatProd: {
                src: [
                    'rfc/aux/header.html',
                    '.build/wamp-processed.md',
                    '.build/footer.html'
                ],
                dest: 'docs/_static/wamp_latest.html'
            },
            concatDev: {
                src: [
                    'rfc/aux/header.html',
                    '.build/wamp-processed.md',
                    'rfc/aux/footer.html'
                ],
                dest: 'docs/_static/wamp_latest.html'
            }
        },
        watch: {
            sources: {
                files: ['Gruntfile.js', 'rfc/aux/header.html', 'rfc/aux/footer.html', 'rfc/**/*.md'],
                tasks: ['clean', 'replace:spec', 'includereplace', 'copy', 'concat:concatDev'],
                options: {
                    reload: true,
                    livereload: true
                }
            }
        }
    });

    grunt.registerTask('default', ['clean', 'replace', 'includereplace', 'copy', 'concat:concatProd']);
};
/**
 * Utility functions for the jenkins pipeline.
 * More about groove for Java dev: http://groovy-lang.org/differences.html
 */

/**
 * Build docker image in the current context.
 * Equivalent for: docker build -t ${tag} .
 * @param tag: tag to be applied
 * @return
 */
def build(String tag) {

    docker.build(tag)
}

/**
 * Build docker image in the given context path.
 * Equivalent for: docker build -f ci/Dockerfile -t ${tag} .
 * @param tag: tag to be applied
 * @param contextPath: location of docker context
 * @return
 */
def build(String tag, String contextPath) {

    docker.build(tag, ' ' + contextPath)
}

/**
 * Deploy docker image to docker registry.
 * @param imageName: image name
 * @param tag: tag to be applied to image
 * @param registryUrl: docker registry url
 * @param credentials: credentials to docker registry
 * @return
 */
def deployImage(String imageName, String tag, String registryUrl, String credentials) {

    docker.withRegistry(registryUrl, credentials) {
        docker.image(imageName).push(tag)
    }
}

return this // this is necessary for the jenkins pipeline load function
